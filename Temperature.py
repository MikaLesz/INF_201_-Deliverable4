"""Temperature class supporting Celsius, fahrenheit, and kelvin"""

from __future__ import annotations

import math

TOLERANCE = 1e-9
_VALID_UNITS = ("C", "F", "K")


class Temperature:
    """A temperature with a value and a unit ("C", "F" or "K")"""

    def __init__(self, value: float, unit: str = "C") -> None:  # unit check first, so a bad unit gives a clear error
        if not isinstance(unit, str) or unit.strip().upper() not in _VALID_UNITS:
            raise ValueError(f"Invalid unit {unit!r}. Use 'C', 'F' og 'K' ")
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("value must be a number (int or float)")
        if not math.isfinite(value):
            raise ValueError("value must be a finite number")

        unit = unit.strip().upper()

        kelvin = self._kelvin_from(float(value), unit)

        if kelvin < -TOLERANCE:
            raise ValueError("temperature cannot be bellow absolute 0")
        
        
        self._value = float(value)
        self._unit = unit


    # read only attributes
    @property
    def value(self) -> float:
        return self._value

    @property
    def unit(self) -> str:
        return self._unit


    # conversions
    @staticmethod
    def _kelvin_from(value: float, unit: str) -> float:
        if unit == "K":
            return value
        if unit == "C":
            return value + 273.15
        return (value - 32) * ( 5 / 9 ) +273.15 # 'F'

    def to_celsius(self) -> float:
        if self._unit == "C":
            return self._value
        if self._unit == "K":
            return self._value - 273.15
        return (self._value - 32) * ( 5 / 9 )

    def to_fahrenheit(self) -> float:
        if self._unit == "F":
            return self._value
        if self._unit == "C":
            return self._value * ( 9 / 5 ) + 32
        return (self._value - 273.15) * ( 9 / 5 ) + 32  # from 'K'

    def to_kelvin(self) -> float:
        return self._kelvin_from(self._value, self._unit)

    def convert_to(self, target_unit: str) -> Temperature:
        if not isinstance(target_unit, str) or target_unit.strip().upper() not in _VALID_UNITS:
            raise ValueError("Invalid target unit. Use 'C', 'F' or 'K'.")

        target = target_unit.strip().upper()

        converters = {
            "C": self.to_celsius,
            "F": self.to_fahrenheit,
            "K": self.to_kelvin,
        }

        return Temperature(converters[target](), target)

    
    # string representations
    def __repr__(self) -> str:
        return f"Temperature({self._value!r}, '{self._unit}')"

    def __str__(self) -> str:
        symbol = "K" if self._unit == "K" else f"°{self._unit}"
        return f"{self._value:.2f} {symbol}"


    # comparisons done in kelvin with the tolerance 1e-9
    def _is_close(self, other: Temperature) -> bool:
        return math.isclose(
            self.to_kelvin(),
            other.to_kelvin(),
            rel_tol=0.0,
            abs_tol=TOLERANCE,
        )

    def __eq__(self, other: object):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self._is_close(other)

    def __ne__(self, other: object):
        if not isinstance(other, Temperature):
            return NotImplemented
        return not self._is_close(other)

    def __lt__(self, other: object):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() < other.to_kelvin() and not self._is_close(other)

    def __le__(self, other: object):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() < other.to_kelvin() or self._is_close(other)

    def __gt__(self, other: object):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() > other.to_kelvin() and not self._is_close(other)

    def __ge__(self, other: object):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() > other.to_kelvin() or self._is_close(other)
