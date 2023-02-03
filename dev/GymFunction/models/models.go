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

type PostMessage struct {
	Gyms []PutGym `json:"gyms"`
}

type PutGym struct {
	Brand    string `json:"brand"`
	Location string `json:"location"`
	BrandId  int    `json:"brandId"`
}
