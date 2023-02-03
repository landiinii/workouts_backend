package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"errors"
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
		var message models.PostMessage
		err = json.Unmarshal([]byte(request.Body), &message)
		if err != nil {
			errorMsg = "Could not parse the request Body"
			return apiResponse(401, models.ErrorBody{ErrorMsg: &errorMsg})
		}
		for _, gym := range message.Gyms {
			if gym.Brand == "" && gym.BrandId == 0 {
				errorMsg = "You need to provide a Brand"
				return apiResponse(401, models.ErrorBody{ErrorMsg: &errorMsg})
			}
			if gym.Location == "" {
				errorMsg = "You need to provide a Name"
				return apiResponse(401, models.ErrorBody{ErrorMsg: &errorMsg})
			}
			if gym.Brand != "" && gym.BrandId == 0 {
				gym.BrandId, err = getBrandId(gym.Brand)
				if err != nil {
					return apiResponse(500, models.ErrorBody{ErrorMsg: &errorMsg})
				}
			}
			err = putGyms(gym.BrandId, gym.Location)
			if err != nil {
				return apiResponse(500, models.ErrorBody{ErrorMsg: &errorMsg})
			}
		}
	}

	// Get list of keywords
	resp.Gyms, err = getGyms()
	if err != nil {
		return apiResponse(500, models.ErrorBody{ErrorMsg: &errorMsg})
	}

	return apiResponse(200, resp)
}

func getBrandId(brand string) (int, error) {
	var brandId int
	// check if brand is there
	err = db.QueryRow("SELECT id from gym_brand where name = $1;", brand).Scan(&brandId)
	if errors.Is(err, sql.ErrNoRows) {
		// Insert new row if not
		insertBrandString := "INSERT INTO gym_brand (name) VALUES ($1) returning id;"
		err := db.QueryRow(insertBrandString, brand).Scan(&brandId)
		if err != nil {
			errorMsg = "Failed to insert new brand to table."
			fmt.Println(err)
			return 0, err
		}
	} else if err != nil {
		errorMsg = "Failed to get gym_brands query."
		fmt.Println(err)
		return 0, err
	}
	return brandId, nil
}

func putGyms(brandId int, loco string) error {
	// check if gym is already there
	var gymId int = 0
	err = db.QueryRow("SELECT id from gym where name = $1 and brand_id = $2;", loco, brandId).Scan(&gymId)
	if gymId != 0 {
		fmt.Println("Gym already exists.")
		return nil
	}
	if errors.Is(err, sql.ErrNoRows) {
		// Insert new row if not
		insertBrandString := "INSERT INTO gym (name, brand_id) VALUES ($1, $2);"
		_, err := db.Exec(insertBrandString, loco, brandId)
		if err != nil {
			errorMsg = fmt.Sprintf("Failed to insert new gym to table: %s, %s, %d", insertBrandString, loco, brandId)
			fmt.Println(err)
			return err
		}
	} else if err != nil {
		errorMsg = "Failed to get gym query."
		fmt.Println(err)
		return err
	}
	return nil
}

func getGymsSQL() string {
	return "SELECT gym.id, concat_ws(' - ', gym.name, gym_brand.name) FROM gym_brand" +
		" JOIN gym ON gym.brand_id=gym_brand.id;"
}

func getGyms() ([]models.Gym, error) {
	getGymQuery := getGymsSQL()
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
