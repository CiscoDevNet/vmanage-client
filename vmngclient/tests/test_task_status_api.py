import unittest
from unittest.mock import patch

from vmngclient.api.task_status_api import Task
from vmngclient.primitives.configuration_dashboard_status import ConfigurationDashboardStatusPrimitives, TaskData


class TestTaskStatusApi(unittest.TestCase):
    @patch("vmngclient.session.vManageSession")
    def setUp(self, mock_session):
        self.task = Task(mock_session, "task_id")
        self.success_response = {
            "data": [
                {
                    "local-system-ip": "local_ip",
                    "statusType": "reboot",
                    "activity": [],
                    "system-ip": "system_ip",
                    "site-id": "siteid",
                    "uuid": "dev-uuid",
                    "@rid": 1211,
                    "personality": "vedge",
                    "processId": "processid",
                    "actionConfig": "",
                    "device-type": "vedge",
                    "action": "reboot",
                    "startTime": 1685440088317,
                    "reachability": "reachable",
                    "order": 0,
                    "vmanageIP": "vmanage_ip",
                    "host-name": "vm1",
                    "version": "vmanage-version",
                    "deviceID": "deviceid",
                    "statusId": "success",
                    "currentActivity": "Done - Reboot",
                    "deviceModel": "vedge-cloud",
                    "validity": "valid",
                    "requestStatus": "received",
                    "status": "Success",
                }
            ],
            "validation": {
                "statusType": "reboot",
                "activity": [],
                "vmanageIP": "vmanage-ip",
                "system-ip": "Validation",
                "deviceID": "Validation",
                "uuid": "Validation",
                "@rid": 747,
                "statusId": "validation_success",
                "processId": "reboot-9fc30834-cc46-47c5-83c4-0b837cf84f1a",
                "actionConfig": "{}",
                "currentActivity": "Done - Validation",
                "action": "reboot",
                "startTime": 1685440057748,
                "requestStatus": "received",
                "status": "Validation success",
                "order": 0,
            },
            "summary": {
                "action": "reboot",
                "name": "Reboot",
                "detailsURL": "/dataservice/device/action/status",
                "startTime": "1685440057829",
                "endTime": "1685440179295",
                "userSessionUserName": "admin",
                "userSessionIP": "10.0.1.1",
                "tenantName": "DefaultTenant",
                "total": 1,
                "status": "done",
                "count": {"Success": 1},
            },
            "isCancelEnabled": True,
            "isParallelExecutionEnabled": True,
        }
        self.empty_data = {
            "data": [],
            "validation": {
                "statusType": "reboot",
                "activity": [],
                "vmanageIP": "vmanage-ip",
                "system-ip": "Validation",
                "deviceID": "Validation",
                "uuid": "Validation",
                "@rid": 747,
                "statusId": "validation_success",
                "processId": "reboot-9fc30834-cc46-47c5-83c4-0b837cf84f1a",
                "actionConfig": "{}",
                "currentActivity": "Done - Validation",
                "action": "reboot",
                "startTime": 1685440057748,
                "requestStatus": "received",
                "status": "Validation success",
                "order": 0,
            },
            "summary": {
                "action": "reboot",
                "name": "Reboot",
                "detailsURL": "/dataservice/device/action/status",
                "startTime": "1685440057829",
                "endTime": "1685440179295",
                "userSessionUserName": "admin",
                "userSessionIP": "user-session-ip",
                "tenantName": "DefaultTenant",
                "total": 1,
                "status": "done",
                "count": {"Success": 1},
            },
            "isCancelEnabled": True,
            "isParallelExecutionEnabled": True,
        }
        self.no_data = {
            "validation": {
                "statusType": "reboot",
                "activity": [],
                "vmanageIP": "ip",
                "system-ip": "Validation",
                "deviceID": "Validation",
                "uuid": "Validation",
                "@rid": 747,
                "statusId": "validation_success",
                "processId": "reboot-9fc30834-cc46-47c5-83c4-0b837cf84f1a",
                "actionConfig": "{}",
                "currentActivity": "Done - Validation",
                "action": "reboot",
                "startTime": 1685440057748,
                "requestStatus": "received",
                "status": "Validation success",
                "order": 0,
            },
            "summary": {
                "action": "reboot",
                "name": "Reboot",
                "detailsURL": "/dataservice/device/action/status",
                "startTime": "1685440057829",
                "endTime": "1685440179295",
                "userSessionUserName": "admin",
                "userSessionIP": "ip",
                "tenantName": "DefaultTenant",
                "total": 1,
                "status": "done",
                "count": {"Success": 1},
            },
            "isCancelEnabled": True,
            "isParallelExecutionEnabled": True,
        }

    @patch.object(Task, "_Task__check_validation_status")
    @patch.object(ConfigurationDashboardStatusPrimitives, "find_status")
    def test_wait_for_completed_success(self, mock_task, mock_validation):
        # Arrange
        mock_task.return_value = TaskData.parse_obj(self.success_response)

        # Act
        answer = self.task.wait_for_completed(interval_seconds=1).result

        # Assert
        self.assertEqual(answer, True)

    @patch.object(Task, "_Task__check_validation_status")
    @patch.object(ConfigurationDashboardStatusPrimitives, "find_status")
    def test_wait_for_completed_empty_data(self, mock_task, mock_validation):
        # Data is empty, and then response is success

        # Arrange
        mock_task.side_effect = [TaskData.parse_obj(self.empty_data), TaskData.parse_obj(self.success_response)]

        # Act
        answer = self.task.wait_for_completed(timeout_seconds=2, interval_seconds=1).result

        # Assert
        self.assertEqual(answer, True)

    @patch.object(Task, "_Task__check_validation_status")
    @patch.object(ConfigurationDashboardStatusPrimitives, "find_status")
    def test_wait_for_completed_no_data(self, mock_task, mock_validation):
        # No data in first call, and then response is success

        # Arrange
        mock_task.side_effect = [TaskData.parse_obj(self.no_data), TaskData.parse_obj(self.success_response)]

        # Act
        answer = self.task.wait_for_completed(timeout_seconds=2, interval_seconds=1).result

        # Assert
        self.assertEqual(answer, True)
