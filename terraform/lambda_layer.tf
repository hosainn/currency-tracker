resource "random_string" "lambda_layer_name_suffix" {
  length  = 2
  upper   = true
  lower   = true
  special = false
}

resource "aws_lambda_layer_version" "common_lambda_layer" {
  filename            = "${path.module}/../lambda_layer/common_layer.zip"
  layer_name          = "common_layer-${random_string.lambda_layer_name_suffix.result}"
  compatible_runtimes = [local.lambda_python_version]
  depends_on          = [null_resource.build_lambda_layer]
}

resource "null_resource" "build_lambda_layer" {
  provisioner "local-exec" {
    when    = create
    command = "python3 ./${path.module}/build_lambda_layer.py"

    environment = {
      LAYER_DIR = "${abspath(path.module)}/../lambda_layer"
    }
  }

  triggers = {
    always_run = timestamp()
  }
}
