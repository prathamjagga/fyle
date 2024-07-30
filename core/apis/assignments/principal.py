from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher

from .schema import AssignmentSchema, AssignmentSubmitSchema, AssignmentGradeSchema
principal_assignment_resources = Blueprint('principal_assignment_resources', __name__)


@principal_assignment_resources.route('/principal/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_all_graded_submitted_assignments(p):
    """Returns graded/submitted assignments"""
    students_assignments = Assignment.get_graded_and_submitted_assignments()
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)

@principal_assignment_resources.route('/principal/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_all_teachers(p):
    """Returns all teachers"""
    teachers = Teacher.get_all()
    teachers = AssignmentSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers)

@principal_assignment_resources.route('/principal/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def regrade(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)

