package models

type ErrorBody struct {
	ErrorMsg *string `json:"error,omitempty"`
}

type Response struct {
	Gyms []Gym `json:"gyms"`
}

type Gym struct {
	Place string `json:"gym"`
	Id    int    `json:"id"`
}
