package models

type ErrorBody struct {
	ErrorMsg *string `json:"error,omitempty"`
}

type Response struct {
	Gyms  []Gym  `json:"gyms"`
	Types []Type `json:"types"`
	Exers []Exer `json:"exercises"`
}

type Gym struct {
	Place string `json:"gym"`
	Id    int    `json:"id"`
}

type Type struct {
	Type string `json:"type"`
	Id   int    `json:"id"`
}

type Exer struct {
	Exer string `json:"exercise"`
	Id   int    `json:"id"`
}
