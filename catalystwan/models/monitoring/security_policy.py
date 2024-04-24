# Copyright 2024 Cisco Systems, Inc. and its affiliates

from pydantic import BaseModel, Field


class DeviceListResponse(BaseModel):
    amp_down: list = Field(..., alias="amp_down")
    amp_up: list = Field(..., alias="amp_up")
    ips_down: list = Field(..., alias="ips_down")
    ips_up: list = Field(..., alias="ips_up")
    urlf_down: list = Field(..., alias="urlf_down")
    urlf_up: list = Field(..., alias="urlf_up")
    zbfw_down: list = Field(..., serialization_alias="zbfw_down", validation_alias="zbfw_down")
    zbfw_up: list = Field(..., serialization_alias="zbfw_up", validation_alias="zbfw_up")