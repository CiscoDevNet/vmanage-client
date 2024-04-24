# Copyright 2024 Cisco Systems, Inc. and its affiliates

from pydantic import BaseModel, Field


class DeviceListResponse(BaseModel):
    data: dict = Field(..., alias="data")

    def get_amp_down(self) -> list:
        return self.data["amp_down"]

    def get_amp_up(self) -> list:
        return self.data["amp_up"]

    def get_ips_down(self) -> list:
        return self.data["ips_down"]

    def get_ips_up(self) -> list:
        return self.data["ips_up"]

    def get_urlf_down(self) -> list:
        return self.data["urlf_down"]

    def get_urlf_up(self) -> list:
        return self.data["urlf_up"]

    def get_zbfw_down(self) -> list:
        return self.data["zbfw_down"]

    def get_zbfw_up(self) -> list:
        return self.data["zbfw_up"]
