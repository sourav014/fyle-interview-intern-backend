from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema, AssignmentGradeSchema

teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments"""
    submitted_assignments_to_teacher = Assignment.get_assignments_submitted_to_teacher(p.teacher_id)
    submitted_assignments_to_teacher_dump = AssignmentSchema().dump(submitted_assignments_to_teacher, many=True)
    return APIResponse.respond(data=submitted_assignments_to_teacher_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def upsert_assignment(p, incoming_payload):
    """Create or Edit an assignment"""
    assignment = AssignmentGradeSchema().load(incoming_payload)

    upserted_assignment = Assignment.upsert_grade(assignment, p)
    
    db.session.commit()
    upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)
    return APIResponse.respond(data=upserted_assignment_dump)
