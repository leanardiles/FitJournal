package com.example.fitjournal_capstone_leandro.data.repository

import com.example.fitjournal_capstone_leandro.data.model.MusclePool
import com.example.fitjournal_capstone_leandro.data.model.RoutineResponse
import com.example.fitjournal_capstone_leandro.data.model.UserExercise

interface IUserRoutineRepository {
    suspend fun getRoutine(): Result<RoutineResponse>
    suspend fun getExercises(): Result<List<UserExercise>>
    // days: day_number -> the per-muscle pools chosen for that day
    suspend fun saveRoutine(days: Map<Int, List<MusclePool>>): Result<Unit>
    suspend fun deleteRoutine(): Result<Unit>
}