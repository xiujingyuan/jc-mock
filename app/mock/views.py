from flask import render_template
from app.mock import mock_backend
from app.models.MockModel import Mock
from app.models.SysProgramDb import SysProgram


@mock_backend.route('/mock', methods=['GET', 'POST'])
def index():

    sys_program = SysProgram.query
    mocks = {}
    for index, link_type_item in enumerate(sys_program):
        mock = Mock.query.filter_by(mock_system=link_type_item.link_type_id)
        mocks[index + 1] = mock
    return render_template(current_app.config["THEME_URL"] +'mock/mock.html', link_type=sys_program, mocks=mocks)


