import json
import math
import typing

import pint

ureg = pint.UnitRegistry()

# The scales to convert to
SCALES = {
    "rideable live steam": 1 / 8,
    "tenth": 1 / 10,
    "twelfth": 1 / 12,
    "unrideable live steam": 1 / 16,
    "dollhouse": 1 / 18,
    "g": 1 / 22.5,
    "54 mm figure": 1 / 32,
    "period ship plan": 1 / 36,
    "die-cast car": 1 / 43,
    "quarter": 1 / 48,
    "small 28mm figure": 1 / 56,
    "large 28mm figure": (5 * ureg.mm) / ureg.foot,
    "25mm figure": 1 / 64,
    "inch figure": 1 / 72,
    "oo": (4 * ureg.mm) / ureg.foot,
    "ho": (3.5 * ureg.mm) / ureg.foot,
    "20mm figure": (10 * ureg.mm) / (3 * ureg.foot),
    "15mm figure": 1 / 100,
    "tt": 1 / 120,
    "12mm figure": 1 / 144,
    "us n": 1 / 160,
    "10mm figure": (10 * ureg.mm) / (6 * ureg.foot),
    "9mm figure": 1 / 200,
    "6mm figure": 1 / 285,
    "nato standard": 1 / 300,
    "t": 1 / 480,
    "ship drawing": 1 / 600,
    "european ship": 1 / 1250,
}

# The quantities to scale
QUANTITIES = {
    "10ft": 10 * ureg.foot,
    "3m": 3 * ureg.m,
    "2m": 2 * ureg.m,
    "5ft": 5 * ureg.foot,
    "1m": 1 * ureg.m,
    "1yd": 3 * ureg.foot,
    "2ft": 2 * ureg.foot,
    "50mm": 50 * ureg.mm,
    "1ft": 1 * ureg.foot,
    "10cm": 10 * ureg.cm,
    "6in": 6 * ureg.inch,
    "5cm": 5 * ureg.cm,
    "1in": 1 * ureg.inch,
    "1/2in": ureg.inch / 2,
    "3/8in": (3 / 8) * ureg.inch,
    "1/4in": ureg.inch / 4,
    "10mm": 1 * ureg.cm,
    "1/8in": ureg.inch / 8,
    "100 thou": 0.1 * ureg.inch,
    "5mm": 5 * ureg.mm,
    "1/16in": ureg.inch / 16,
    "50 thou": 0.05 * ureg.inch,
    "1mm": 1 * ureg.mm,
    "1/32": ureg.inch / 32,
    "10 thou": 0.01 * ureg.inch,
    ".1mm": 0.1 * ureg.mm,
    "1 thou": 0.001 * ureg.inch,
    ".01mm": 0.01 * ureg.mm,
    "10ga steel": 0.1345 * ureg.inch,
    "12ga steel": 0.1046 * ureg.inch,
    "16ga steel": 0.0598 * ureg.inch,
    "22ga steel": 0.0299 * ureg.inch,
    "10ga al / brass": 0.1019 * ureg.inch,
    "12ga al / brass": 0.08081 * ureg.inch,
    "16ga al / brass": 0.05082 * ureg.inch,
    "22ga al / brass": 0.02535 * ureg.inch,
    "30ga al / brass": 0.01003 * ureg.inch,
    "0 awg": 0.3648 * ureg.inch,
    "8 awg": 0.1285 * ureg.inch,
    "12 awg": 0.0808 * ureg.inch,
    "18 awg": 0.0403 * ureg.inch,
}


def to_feet_and_inches(
    value: pint.Quantity,
) -> typing.Tuple[pint.Quantity, pint.Quantity]:
    """Split a quantity into feet & inches

    Args:
        value: The quantity to split
    """
    feet = math.floor(value.to(ureg.foot).magnitude) * ureg.foot
    inches = (value - feet).to(ureg.inch)

    return feet, inches


def format_quantity(value: pint.Quantity) -> str:
    """Pretty-print a quantity

    The value will be presented in feet & inches if it is larger than 1ft,
    else it will be presented in inche. Inches will be rounded to tenthousandths,
    and omitted from feet pairs if they would print 0s.

    Args:
        value: The quantity to prit
    """
    if value > (1 * ureg.foot):
        feet, inches = to_feet_and_inches(value)

        return f"{feet:d~}" + (
            f" {inches:0.4f~}" if inches >= (0.0001 * ureg.inch) else ""
        )
    else:
        return f"{value.to(ureg.inch):0.4f~}"


SCALED_QUANTITIES = {
    scale_name: {
        # The that a scale representation of an object would be
        "at_scale": {
            quantity_name: quantity_value * scale_ratio
            for quantity_name, quantity_value in QUANTITIES.items()
        },
        # The size an object would be, when used in a scale model
        "in_scale": {
            quantity_name: quantity_value / scale_ratio
            for quantity_name, quantity_value in QUANTITIES.items()
        },
    }
    for scale_name, scale_ratio in SCALES.items()
}


with open("scaled_quantities.json", "w", encoding="utf-8") as json_out_file:
    json.dump(
        {
            scale_name: {
                scale_subtype: {
                    quantity_name: format_quantity(quantity_value)
                    for quantity_name, quantity_value in sorted(
                        scaled_quantities[scale_subtype].items(),
                        key=lambda scaled_value_pair: scaled_value_pair[1],
                        reverse=True,
                    )
                    if quantity_value >= (0.0001 * ureg.inch)
                    and quantity_value <= (15 * ureg.foot)
                }
                for scale_subtype in scaled_quantities
            }
            for scale_name, scaled_quantities in sorted(
                SCALED_QUANTITIES.items(),
                key=lambda scaled_quantities_pair: (
                    SCALES[scaled_quantities_pair[0]]
                    if isinstance(SCALES[scaled_quantities_pair[0]], float)
                    else SCALES[scaled_quantities_pair[0]].to_base_units().magnitude
                ),
            )
        },
        json_out_file,
        ensure_ascii=False,
        indent=2,
    )
