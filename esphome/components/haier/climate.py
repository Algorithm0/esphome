from esphome.components import climate
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.components.climate import ClimateSwingMode
from esphome.components.climate import ClimatePreset
from esphome.const import CONF_ID, CONF_SUPPORTED_SWING_MODES, CONF_SUPPORTED_PRESETS

DEPENDENCIES = ["uart"]

haier_ns = cg.esphome_ns.namespace("haier")
HaierClimate = haier_ns.class_(
    "HaierClimate", climate.Climate, cg.PollingComponent, uart.UARTDevice
)

ALLOWED_CLIMATE_SWING_MODES = {
    "OFF": ClimateSwingMode.CLIMATE_SWING_OFF,
    "BOTH": ClimateSwingMode.CLIMATE_SWING_BOTH,
    "VERTICAL": ClimateSwingMode.CLIMATE_SWING_VERTICAL,
    "HORIZONTAL": ClimateSwingMode.CLIMATE_SWING_HORIZONTAL,
}

ALLOWED_CLIMATE_PRESETS = {
    "NONE": ClimatePreset.CLIMATE_PRESET_NONE,
    "COMFORT": ClimatePreset.CLIMATE_PRESET_COMFORT,
}

validate_swing_modes = cv.enum(ALLOWED_CLIMATE_SWING_MODES, upper=True)
validate_presets = cv.enum(ALLOWED_CLIMATE_PRESETS, upper=True)

CONFIG_SCHEMA = cv.All(
    climate.CLIMATE_SCHEMA.extend(
        {
            cv.GenerateID(): cv.declare_id(HaierClimate),
            cv.Optional(CONF_SUPPORTED_SWING_MODES): cv.ensure_list(
                validate_swing_modes
            ),
            cv.Optional(CONF_SUPPORTED_PRESETS): cv.ensure_list(
                validate_presets
            ),
        }
    )
    .extend(cv.polling_component_schema("5s"))
    .extend(uart.UART_DEVICE_SCHEMA),
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await climate.register_climate(var, config)
    await uart.register_uart_device(var, config)
    if CONF_SUPPORTED_SWING_MODES in config:
        cg.add(var.set_supported_swing_modes(config[CONF_SUPPORTED_SWING_MODES]))
    if CONF_SUPPORTED_PRESETS in config:
        cg.add(var.set_supported_presets(config[CONF_SUPPORTED_PRESETS]))
