/*
TODO: Go into the environment before hand, 
into parameter store in the systems manager
and create a Secure String value that contains
the db_password you want to use located at 
"/${var.prefix}/password/master"

From an error message I got: "Only printable ASCII characters besides '/', '@', '"', ' ' may be used."
*/

data "aws_ssm_parameter" "db_password" {
  name = "/${var.prefix}/password/master"
}

// to access password: data.aws_ssm_parameter.db_password.value




// VPC identifiers (dont need to do anything for these)
// vpc_id = data.aws_vpc.vpc.id
// subnet_ids = tolist(data.aws_subnet_ids.public.ids)
data "aws_caller_identity" "current" {}

variable "vpc_name" {
  type    = string
  default = "landiinii-oregon"
}

data "aws_vpc" "vpc" {
  default = false
  filter {
    name   = "tag:Name"
    values = [var.vpc_name]
  }
}



data "aws_subnet_ids" "public" {
  vpc_id = data.aws_vpc.vpc.id
  filter {
    name = "tag:Name"
    values = [
      "*-public-*",
    ]
  }
}


// Current accout id
// account_id = data.aws_caller_identity.current.account_id
