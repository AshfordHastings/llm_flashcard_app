
data "azurerm_client_config" "current" {}
data "azurerm_subscription" "primary" {}

locals {
  subscription_id = data.azurerm_subscription.primary.id
  prefix          = "fcard"
}


resource "azurerm_resource_group" "rg" {
  name     = "${local.prefix}-rg"
  location = "East US 2"
}