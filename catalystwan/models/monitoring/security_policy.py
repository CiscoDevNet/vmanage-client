# Copyright 2024 Cisco Systems, Inc. and its affiliates

from pydantic import BaseModel, Field


class DeviceListResponse(BaseModel):
    data: dict = Field(..., alias="data")

    def get_amp_down(self) -> list:
        return self.data["amp_down"]
        # amp_down: list = Field(..., alias="amp_down")
    def get_amp_up(self) -> list:
        return self.data["amp_up"]
        # amp_up: list = Field(..., alias="amp_up")
    def get_ips_down(self) -> list:
        return self.data["ips_down"]
        # ips_down: list = Field(..., alias="ips_down")
    def get_ips_up(self) -> list:
        return self.data["ips_up"]
        # ips_up: list = Field(..., alias="ips_up")
    def get_urlf_down(self) -> list:
        return self.data["urlf_down"]
        # urlf_down: list = Field(..., alias="urlf_down")
    def get_urlf_up(self) -> list:
        return self.data["urlf_up"]
        # urlf_up: list = Field(..., alias="urlf_up")
    def get_zbfw_down(self) -> list:
        return self.data["zbfw_down"]
        # zbfw_down: list = Field(..., serialization_alias="zbfw_down", validation_alias="zbfw_down")
    def get_zbfw_up(self) -> list:
        return self.data["zbfw_up"]
        # zbfw_up: list = Field(..., serialization_alias="zbfw_up", validation_alias="zbfw_up")