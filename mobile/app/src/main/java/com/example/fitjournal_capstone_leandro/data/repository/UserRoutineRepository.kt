package com.example.fitjournal_capstone_leandro.data.repository

import com.example.fitjournal_capstone_leandro.data.model.RoutineResponse
import com.example.fitjournal_capstone_leandro.data.model.RoutineSetupRequest
import com.example.fitjournal_capstone_leandro.data.model.TrainingDayMuscleRequest
import com.example.fitjournal_capstone_leandro.data.model.TrainingDayRequest
import com.example.fitjournal_capstone_leandro.data.local.TokenManager
import com.example.fitjournal_capstone_leandro.data.network.RetrofitClient

class UserRoutineRepository(
    private val tokenManager: TokenManager
) : IUserRoutineRepository {
    private val apiService = RetrofitClient.apiService

    companion object {
        // Default per-session exercise count for a per_muscle day. Generation
        // draws up to this many from the muscle's pool (fewer if the pool is
        // smaller), so this is safe even for muscles with only one exercise.
        private const val DEFAULT_EXERCISE_COUNT = 3
    }

    /**
     * Get user's current routine (new training-day shape).
     */
    override suspend fun getRoutine(): Result<RoutineResponse> {
        return try {
            val userId = tokenManager.getUserId()
            if (userId == -1) return Result.failure(Exception("No user logged in"))
            val routine = apiService.getRoutine(userId)
            Result.success(routine)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Save user's routine.
     *
     * The mobile app currently builds per_muscle days only: for each day the
     * user picks muscle groups, and we auto-include every exercise the user
     * owns for those muscles as the day's pool (with a default per-session
     * count). Manual days / per-day type selection / grouping come with the
     * parity pass.
     *
     * @param daysPerWeek kept for call-site compatibility; the backend derives
     *                    days_per_week from the number of days, so it's unused.
     * @param routineDays day_number -> chosen muscle groups for that day.
     */
    override suspend fun saveRoutine(
        daysPerWeek: Int,
        routineDays: Map<Int, List<String>>
    ): Result<Unit> {
        return try {
            val userId = tokenManager.getUserId()
            if (userId == -1) return Result.failure(Exception("No user logged in"))

            // The pool for each muscle is every exercise the user owns for it.
            val exerciseIdsByMuscle: Map<String, List<Int>> = apiService.getExercises(userId)
                .groupBy { it.exercise_muscle_group }
                .mapValues { (_, list) -> list.map { it.exercise_id } }

            val days = routineDays.toSortedMap().map { (dayNumber, muscles) ->
                val poolIds = muscles
                    .flatMap { exerciseIdsByMuscle[it].orEmpty() }
                    .distinct()

                TrainingDayRequest(
                    day_number = dayNumber,
                    day_type = "per_muscle",
                    name = null,
                    muscles = muscles.map {
                        TrainingDayMuscleRequest(
                            muscle_group = it,
                            exercise_count = DEFAULT_EXERCISE_COUNT
                        )
                    },
                    exercise_ids = poolIds
                )
            }

            apiService.saveRoutine(userId, RoutineSetupRequest(days = days))
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Delete user's routine
     */
    override suspend fun deleteRoutine(): Result<Unit> {
        return try {
            val userId = tokenManager.getUserId()
            if (userId == -1) return Result.failure(Exception("No user logged in"))
            apiService.deleteRoutine(userId)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}