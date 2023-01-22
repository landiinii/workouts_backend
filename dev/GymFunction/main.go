package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"os"

	models "main/models"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	_ "github.com/lib/pq"
)

var (
	errorMsg    string
	err         error
	resp        models.Response
	db          *sql.DB
	db_host     = os.Getenv("DB_HOST")
	db_port     = 5432
	db_user     = os.Getenv("DB_USER")
	db_password = os.Getenv("DB_PASSWORD")
	db_name     = os.Getenv("DB_NAME")
)

func main() {
	lambda.Start(handler)
}

func handler(ctx context.Context, request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {

	// Instantiate DB connection in global variable `db`
	err = initiateDatabase()
	if err != nil {
		return apiResponse(500, models.ErrorBody{ErrorMsg: &errorMsg})
	}
	defer db.Close()

	if request.HTTPMethod == "POST" {

	}

	// Get list of keywords
	resp.Gyms, err = getGyms()
	if err != nil {
		return apiResponse(500, models.ErrorBody{ErrorMsg: &errorMsg})
	}

	return apiResponse(200, resp)
}

func gymSQL() string {
	return "SELECT gym.id, concat_ws(' - ', gym.name, gym_brand.name) FROM gym_brand" +
		" JOIN gym ON gym.brand_id=gym_brand.id;"
}

func getGyms() ([]models.Gym, error) {
	getGymQuery := gymSQL()
	rows, err := db.Query(getGymQuery)
	if err != nil {
		errorMsg = "Failed to execute get gyms query."
		fmt.Println(err)
		return nil, err
	}
	defer rows.Close()

	gyms := make([]models.Gym, 0)
	for rows.Next() {
		var term string
		var id int
		if err := rows.Scan(&id, &term); err != nil {
			errorMsg = "Failed to scan term from gyms query."
			fmt.Println(err)
			return nil, err
		}
		gyms = append(gyms, models.Gym{Place: term, Id: id})
	}
	if err = rows.Err(); err != nil {
		errorMsg = "Failed to iterate rows from gyms query."
		fmt.Println(err)
		return nil, err
	}

	return gyms, nil
}

func initiateDatabase() error {
	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		db_host, db_port, db_user, db_password, db_name)

	db, err = sql.Open("postgres", psqlInfo)
	if err != nil {
		fmt.Println(err)
		errorMsg = "Failed to initialize the DB."
		return err
	}

	err = db.Ping()
	if err != nil {
		db.Close()
		fmt.Println(err)
		errorMsg = "Failed to connect to the DB."
		return err
	}
	return nil
}

func apiResponse(status int, body interface{}) (events.APIGatewayProxyResponse, error) {
	resp := events.APIGatewayProxyResponse{Headers: map[string]string{
		"Content-Type":                 "application/json",
		"Access-Control-Allow-Headers": "*",
		"Access-Control-Allow-Origin":  "*",
		"Access-Control-Allow-Methods": "*",
	}}
	resp.StatusCode = status

	stringBody, _ := json.Marshal(body)
	resp.Body = string(stringBody)

	return resp, nil
}
