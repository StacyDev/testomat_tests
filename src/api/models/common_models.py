from pydantic import BaseModel


class RequestMixin(BaseModel):
    def build(self):
        return self.model_dump(exclude_unset=True, by_alias=True)
