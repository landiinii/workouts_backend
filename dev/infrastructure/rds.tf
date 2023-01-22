resource "aws_db_instance" "DB" {
  allocated_storage               = 20
  engine                          = "postgres"
  engine_version                  = "13.7"
  instance_class                  = "db.t3.micro"
  identifier                      = var.prefix
  name                            = var.prefix
  username                        = "postgres"
  password                        = data.aws_ssm_parameter.db_password.value
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  auto_minor_version_upgrade      = true
  max_allocated_storage           = 20
  storage_encrypted               = true
  publicly_accessible             = true
  storage_type                    = "gp2"
  db_subnet_group_name            = "default-${data.aws_vpc.vpc.id}"
  skip_final_snapshot             = true
  copy_tags_to_snapshot           = true
  performance_insights_enabled    = true
  vpc_security_group_ids          = [aws_security_group.WorkoutsSecurityGroup.id]
}

resource "aws_security_group" "WorkoutsSecurityGroup" {
  name   = "${var.prefix}_sg"
  vpc_id = data.aws_vpc.vpc.id

  ingress {
    protocol    = "tcp"
    self        = true
    from_port   = 5432
    to_port     = 5432
    description = ""
  }
  ingress {
    protocol    = "tcp"
    cidr_blocks = ["24.11.35.96/32"]
    from_port   = 5432
    to_port     = 5432
    description = "AF Townhome"
  }


  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
