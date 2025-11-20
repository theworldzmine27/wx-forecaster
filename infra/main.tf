locals {
  app_name = "wx-forecaster"
  env      = var.env
  prefix   = "${local.app_name}-${local.env}"
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.prefix}-rg"
  location = var.location
}

resource "azurerm_storage_account" "sa" {
  name                     = replace("${local.prefix}sa", "-", "")
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_application_insights" "ai" {
  name                = "${local.prefix}-ai"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  application_type    = "web"
}

resource "azurerm_service_plan" "plan" {
  name                = "${local.prefix}-asp"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_function_app" "func" {
  name                       = "${local.prefix}-func"
  resource_group_name        = azurerm_resource_group.rg.name
  location                   = var.location
  storage_account_name       = azurerm_storage_account.sa.name
  storage_account_access_key = azurerm_storage_account.sa.primary_access_key
  service_plan_id            = azurerm_service_plan.plan.id
  app_settings = {
    FUNCTIONS_WORKER_RUNTIME        = "python"
    AzureWebJobsStorage             = azurerm_storage_account.sa.primary_connection_string
    APPINSIGHTS_INSTRUMENTATIONKEY  = azurerm_application_insights.ai.instrumentation_key
    WEATHERGOV_USER_AGENT           = var.weathergov_user_agent
    DEFAULT_POINTS                  = var.default_points
  }
}
