package com.example.fitjournal_capstone_leandro.data.model

// A per-muscle pool for saving a per_muscle day: which exercises are in the
// pool for this muscle, and how many to draw per session.
data class MusclePool(
    val muscle_group: String,
    val exercise_ids: List<Int>,
    val exercise_count: Int
)