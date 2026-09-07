package com.example.fitjournal_capstone_leandro.data.model

// One day's save payload from the routine editor. A day is either per_muscle
// (muscle pools + counts) or manual (a flat exercise list).
data class DaySave(
    val day_type: String,                        // "per_muscle" | "manual"
    val pools: List<MusclePool> = emptyList(),   // per_muscle days
    val exercise_ids: List<Int> = emptyList()    // manual days
)