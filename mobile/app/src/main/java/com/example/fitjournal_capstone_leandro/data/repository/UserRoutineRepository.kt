package com.example.fitjournal_capstone_leandro.data.repository

import com.example.fitjournal_capstone_leandro.data.model.MusclePool
import com.example.fitjournal_capstone_leandro.data.model.RoutineResponse
import com.example.fitjournal_capstone_leandro.data.model.RoutineSetupRequest
import com.example.fitjournal_capstone_leandro.data.model.TrainingDayMuscleRequest
import com.example.fitjournal_capstone_leandro.data.model.TrainingDayRequest
import com.example.fitjournal_capstone_leandro.data.model.UserExercise
import com.example.fitjournal_capstone_leandro.data.local.TokenManager
import com.example.fitjournal_capstone_leandro.data.network.RetrofitClient

class UserRoutineRepository(
    private val tokenManager: TokenManager
) : IUserRoutineRepository {
    private val apiService = RetrofitClient.apiService

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
     * The user's exercise library — used to populate the routine editor's
     * exercise picker (grouped by muscle by the caller).
     */
    override suspend fun getExercises(): Result<List<UserExercise>> {
        return try {
            val userId = tokenManager.getUserId()
            if (userId == -1) return Result.failure(Exception("No user logged in"))
            Result.success(apiService.getExercises(userId))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Save the user's routine. The editor now sends an explicit per-muscle pool
     * (the chosen exercises) and a per-muscle count for each day, so this just
     * maps that into the training-day request shape. per_muscle days only.
     *
     * @param days day_number -> the per-muscle pools chosen for that day.
     */
    override suspend fun saveRoutine(days: Map<Int, List<MusclePool>>): Result<Unit> {
        return try {
            val userId = tokenManager.getUserId()
            if (userId == -1) return Result.failure(Exception("No user logged in"))

            val dayRequests = days.toSortedMap().map { (dayNumber, pools) ->
                TrainingDayRequest(
                    day_number = dayNumber,
                    day_type = "per_muscle",
                    name = null,
                    muscles = pools.map {
                        TrainingDayMuscleRequest(
                            muscle_group = it.muscle_group,
                            exercise_count = it.exercise_count
                        )
                    },
                    exercise_ids = pools.flatMap { it.exercise_ids }.distinct()
                )
            }

            apiService.saveRoutine(userId, RoutineSetupRequest(days = dayRequests))
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