from typing import Any, List

from starlette_admin import action
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.fields import StringField
from starlette.datastructures import FormData
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette_admin.exceptions import ActionFailed

from museums.models.exposition_tables import Exposition

class ExpositionView(ModelView):  

    actions = ["redirect"]  # `delete` function is added by default
    fields = [  
        "id",   
        StringField("museum_id", label="museum_id", read_only=True),
        "entity",  
        "branch",
        "showcase",
        "history",
        "webpage",
        #"visitors",
        "period",
        "price",
        "created_at",
        "updated_at",   
    ]  

    async def before_create(
        self,
        request: Request,
        data: dict[str, Any],
        exposition: Exposition,
    ):  
        #admin_user = request.state.user  
        #exposition.owner_id = admin_user["id"]
        pass

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