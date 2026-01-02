from typing import Any, List, Dict

from starlette_admin import action
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.fields import StringField
from starlette.datastructures import FormData
from starlette_admin._types import RequestAction
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette_admin.exceptions import ActionFailed

from starlette_admin import BaseField  # development
from dataclasses import dataclass  # development

from museums.models.museum_tables import Category, Location, Museum


class CategoryView(ModelView):  
    fields = [  
        "id",   
        "category",   
    ]  


class LocationView(ModelView):  
    fields = [  
        "id",   
        "location",   
    ]

class MuseumView(ModelView):
    
    #page_size_options = [0, 5, 25, 100, 500]
    #render_function_key: str = "mycustomkey"
    actions = ["redirect", "delete"]  # `delete` function is added by default
    #row_actions_display_type = RowActionsDisplayType.ICON_LIST  # RowActionsDisplayType.DROPDOWN
    
    fields = [
        "id",
        "entity",
        "title",
        "address",
        "category_id",
        "location_id",
        "inn",
        "affiliation",
        "submission",
        "timezone",
        "teg",
        "description",
        "website",
        "email",
        "eipsk",
        "service_name",
        "updated_at",
    ]

    #@action(
        #name="download_csv",
        #text="Mark selected articles as published",
        #confirmation="Are you sure you want to mark selected articles as published ?",
        #submit_btn_text="Yes, proceed",
        #submit_btn_class="btn-success",
        #form="""
        #<form>
            #<div class="mt-3">
                #<input type="text" class="form-control" name="example-text-input" placeholder="Enter value">
            #</div>
        #</form>
        #""",
    #)
    #async def download_csv_action(self, request: Request, pks: List[Any]) -> str:
        # Write your logic here

        #data: FormData = await request.form()
        #user_input = data.get("example-text-input")

        #if False:
            # Display meaningfully error
            #raise ActionFailed("Sorry, We can't proceed this action now.")
        # Display successfully message
        #return "{} articles were successfully marked as published".format(len(pks))

     # For custom response
    @action(
        name="redirect",
        text="Redirect",
        custom_response=True,
        confirmation="Fill the form",
        form='''
        <form>
            <div class="mt-3">
                <input type="text" class="form-control" name="value" placeholder="Enter value">
            </div>
        </form>
        '''
    )
    async def redirect_action(self, request: Request, pks: List[Any]) -> Response:
        data = await request.form()
        return RedirectResponse(f"https://example.com/?value={data['value']}")


@dataclass
class CustomField(BaseField):
    render_function_key: str = "mycustomkey"
    form_template: str = "forms/custom.html"
    display_template: str = "displays/custom.html"

    async def parse_form_data(self, request: Request, form_data: FormData) -> Any:
        return form_data.get(self.name)

    async def serialize_value(self, request: Request, value: Any, action: RequestAction) -> Any:
        return value

    def dict(self) -> Dict[str, Any]:
        print(f"DICT: {super().dict()}")
        return super().dict()
