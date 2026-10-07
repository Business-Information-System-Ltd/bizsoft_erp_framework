import json

from pathlib import Path


class LocationTypeService:

    @staticmethod
    def get_config_path():

        return (
            Path(__file__)
            .resolve()
            .parent
            .parent
            / "config"
            / "location_types.json"
        )


    @classmethod
    def load_config(cls):

        file_path = cls.get_config_path()


        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    @classmethod
    def get_dynamic_fields(cls, location_type):

        config = cls.load_config()


        location_types = config.get(
            "location_types",
            {}
        )


        field_groups = config.get(
            "field_groups",
            {}
        )


        type_config = location_types.get(
            location_type
        )


        if not type_config:

            return None


        field_group_code = type_config.get(
            "field_group"
        )


        field_group = field_groups.get(
            field_group_code
        )


        if not field_group:

            return None


        return field_group