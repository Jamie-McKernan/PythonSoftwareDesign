from src.design_patterns.specification.employee_specification import (
    BelongsToDepartment,
    DevelopmentRaiseEligibility,
    FinanceRaiseEligibility,
    HadValidName,
    HrRaiseEligibility,
    IsValidWorkingAge,
    MatchesHiringCriteria,
    SalesRaiseEligibility,
)
from src.design_patterns.specification.supplement import (
    Department,
    Employee,
    InvalidEmployeeError,
)


# anti-pattern
def hire_new_employee_anti_pattern(
    name: str, age: int, department: Department
) -> Employee:
    new_employee = Employee(name, age, department)

    if (
        new_employee.age < 18
        or new_employee.age > 99
        or new_employee.department == Department.SALES
        or new_employee.name == ""
    ):
        raise InvalidEmployeeError()

    return new_employee


def is_employee_eligible_for_a_raise_anti_pattern(employee: Employee) -> bool:
    if employee.age < 18 or employee.age > 99:
        return False

    if employee.department == Department.SALES:
        if employee.salary < 10_000:
            return False

        if employee.salary >= 10_000:
            if employee.age >= 75:
                return False
            else:
                return True

    elif employee.department == Department.FINANCE:
        if employee.salary > 85_000:
            return False
        return True

    elif employee.department == Department.DEVELOPMENT:
        return True

    elif employee.department == Department.HR:
        for year in employee.previous_bonus_years:
            if year == 2022:
                return False
        return True

    return False


# best practice
def hire_new_employee_simple(name: str, age: int, department: Department) -> Employee:
    hiring_specification = MatchesHiringCriteria()
    new_employee = Employee(name, age, department)

    if hiring_specification.is_satisfied_by(new_employee):
        return new_employee

    raise InvalidEmployeeError()


def hire_new_employee_granular(name: str, age: int, department: Department) -> Employee:
    hiring_specification = (
        IsValidWorkingAge() & HadValidName() & -BelongsToDepartment(Department.SALES)
    )

    new_employee = Employee(name, age, department)

    if hiring_specification.is_satisfied_by(new_employee):
        return new_employee

    raise InvalidEmployeeError()


def is_employee_eligible_for_a_raise(employee: Employee) -> bool:
    raise_specification = (
        SalesRaiseEligibility()
        | FinanceRaiseEligibility()
        | DevelopmentRaiseEligibility()
        | HrRaiseEligibility()
    ) & IsValidWorkingAge()

    return raise_specification.is_satisfied_by(employee)
