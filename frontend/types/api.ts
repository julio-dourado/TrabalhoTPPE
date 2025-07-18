// Tipos baseados na OpenAPI
export interface User {
  id: number;
  name: string;
  email: string;
  birth_date?: string;
  gender: Gender;
  height_cm?: number;
  weight_kg?: number;
  activity_level: ActivityLevel;
  main_goal: FitnessGoal;
  training_experience_years: number;
  bio?: string;
  target_weight_kg?: number;
  is_active: boolean;
  is_premium: boolean;
  created_at: string;
  updated_at?: string;
}

export interface UserCreate {
  name: string;
  email: string;
  password: string;
  birth_date?: string;
  gender?: Gender;
  height_cm?: number;
  weight_kg?: number;
  activity_level?: ActivityLevel;
  main_goal?: FitnessGoal;
  training_experience_years?: number;
  bio?: string;
  target_weight_kg?: number;
}

export interface UserUpdate {
  name?: string;
  password?: string;
  birth_date?: string;
  gender?: Gender;
  height_cm?: number;
  weight_kg?: number;
  activity_level?: ActivityLevel;
  main_goal?: FitnessGoal;
  training_experience_years?: number;
  bio?: string;
  target_weight_kg?: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user_id: number;
}

export interface UserRegistrationRequest {
  name: string;
  email: string;
  password: string;
  password_confirm: string;
}

export interface Exercise {
  id: number;
  name: string;
  muscle_group: MuscleGroup;
  difficulty: Difficulty;
  sets: number;
  reps: number;
  comment?: string;
  instructions?: string;
  rest_time_sec: number;
  is_compound: boolean;
  equipment?: string;
  exercise_type: ExerciseType;
  with_weight_details?: WithWeightDetails;
  without_weight_details?: WithoutWeightDetails;
  created_at: string;
  updated_at?: string;
}

export interface ExerciseCreate {
  name: string;
  muscle_group: MuscleGroup;
  difficulty: Difficulty;
  sets: number;
  reps: number;
  comment?: string;
  instructions?: string;
  rest_time_sec: number;
  is_compound: boolean;
  equipment?: string;
  exercise_type: ExerciseType;
  with_weight_details?: WithWeightDetailsCreate;
  without_weight_details?: WithoutWeightDetailsCreate;
}

export interface WithWeightDetails {
  id: number;
  exercise_id: number;
  weight_kg: number;
  max_weight_kg?: number;
  suggested_increment_kg: number;
  created_at: string;
  updated_at?: string;
}

export interface WithWeightDetailsCreate {
  weight_kg: number;
  max_weight_kg?: number;
  suggested_increment_kg: number;
}

export interface WithoutWeightDetails {
  id: number;
  exercise_id: number;
  duration_sec: number;
  distance_m: number;
  target_speed: number;
  intensity_level: number;
  created_at: string;
  updated_at?: string;
}

export interface WithoutWeightDetailsCreate {
  duration_sec?: number;
  distance_m?: number;
  target_speed?: number;
  intensity_level?: number;
}

export interface Training {
  id: number;
  name: string;
  description?: string;
  category: TrainingCategory;
  estimated_duration_min: number;
  user_id: number;
  status: TrainingStatus;
  actual_duration_min?: number;
  calories_burned?: number;
  total_volume_kg?: number;
  perceived_difficulty?: number;
  satisfaction?: number;
  observations?: string;
  created_at: string;
  updated_at?: string;
  started_at?: string;
  finished_at?: string;
  exercises: Exercise[];
}

export interface TrainingCreate {
  name: string;
  description?: string;
  category: TrainingCategory;
  estimated_duration_min: number;
  exercises?: ExerciseCreate[];
}

export interface TrainingUpdate {
  name?: string;
  description?: string;
  category?: TrainingCategory;
  estimated_duration_min?: number;
  status?: TrainingStatus;
  exercises?: number[];
  actual_duration_min?: number;
  calories_burned?: number;
  total_volume_kg?: number;
  perceived_difficulty?: number;
  satisfaction?: number;
  observations?: string;
}

export interface TrainingStatistics {
  total_trainings: number;
  total_duration_min: number;
  total_calories_burned: number;
  total_volume_kg: number;
  actual_duration_min?: number;
  average_satisfaction: number;
  average_difficulty: number;
  completed_trainings: number;
  favorite_category?: TrainingCategory;
}

// Enums
export enum Gender {
  MALE = "masculino",
  FEMALE = "feminino",
  OTHER = "outro",
  NOT_INFORMED = "nao_informado"
}

export enum ActivityLevel {
  SEDENTARY = "sedentario",
  LIGHT = "leve",
  MODERATE = "moderado",
  INTENSE = "intenso",
  VERY_INTENSE = "muito_intenso"
}

export enum FitnessGoal {
  WEIGHT_LOSS = "perda_peso",
  MUSCLE_GAIN = "ganho_massa",
  GENERAL_HEALTH = "saude_geral",
  STRENGTH = "forca",
  ENDURANCE = "resistencia"
}

export enum MuscleGroup {
  CHEST = "PEITO",
  BACK = "COSTAS",
  SHOULDERS = "OMBROS",
  BICEPS = "BICEPS",
  TRICEPS = "TRICEPS",
  LEGS = "PERNAS",
  GLUTES = "GLUTEOS",
  ABDOMEN = "ABDOMEN",
  CALVES = "PANTURRILHA",
  FOREARMS = "ANTEBRACO",
  CARDIO = "CARDIO",
  FULL_BODY = "CORPO_INTEIRO"
}

export enum Difficulty {
  BEGINNER = "INICIANTE",
  INTERMEDIATE = "INTERMEDIARIO",
  ADVANCED = "AVANCADO"
}

export enum ExerciseType {
  WITH_WEIGHT = "COM_PESO",
  WITHOUT_WEIGHT = "SEM_PESO"
}

export enum TrainingCategory {
  STRENGTH = "FORCA",
  CARDIO = "CARDIO",
  FLEXIBILITY = "FLEXIBILIDADE",
  FUNCTIONAL = "FUNCIONAL",
  ENDURANCE = "RESISTENCIA",
  SPORTS = "ESPORTES",
  REHABILITATION = "REABILITACAO"
}

export enum TrainingStatus {
  PLANNED = "PLANEJADO",
  IN_PROGRESS = "EM_ANDAMENTO",
  COMPLETED = "CONCLUIDO",
  PAUSED = "PAUSADO",
  CANCELLED = "CANCELADO"
} 