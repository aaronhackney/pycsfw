import logging

log = logging.getLogger(__name__)


class SerializeObjects:
    @staticmethod
    def _serialize_objects(obj_list: list) -> list:
        serializable_objs = []
        for i, net_obj in enumerate(obj_list):
            obj_list[i].metadata = None
            serializable_objs.append(obj_list[i].dict(exclude_unset=True))
        return serializable_objs

    @staticmethod
    def _serialize_object(obj: object) -> object:
        obj.metadata = None
        return obj.dict(exclude_unset=True)
