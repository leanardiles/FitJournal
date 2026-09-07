package com.example.fitjournal_capstone_leandro.data.repository

import com.example.fitjournal_capstone_leandro.data.model.DaySave
import com.example.fitjournal_capstone_leandro.data.model.RoutineResponse
import com.example.fitjournal_capstone_leandro.data.model.UserExercise

interface IUserRoutineRepository {
    suspend fun getRoutine(): Result<RoutineResponse>
    suspend fun getExercises(): Result<List<UserExercise>>
    // days: day_number -> that day's save payload (per_muscle pools or manual list)
    suspend fun saveRoutine(days: Map<Int, DaySave>): Result<Unit>
    suspend fun deleteRoutine(): Result<Unit>
}