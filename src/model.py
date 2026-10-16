"""A deliberately partial reconstruction of specified medieval provisions.

Outputs describe individual provisions, never a person's overall legal freedom.
None represents an unresolved historical predicate, rather than False.
"""
from dataclasses import dataclass, replace
from typing import Optional

Truth = Optional[bool]

def conjunction(*values: Truth) -> Truth:
    if False in values:
        return False
    return None if None in values else True

def negation(value: Truth) -> Truth:
    return None if value is None else not value

def disjunction(*values: Truth) -> Truth:
    return negation(conjunction(*(negation(x) for x in values)))

@dataclass(frozen=True)
class Recruitment:
    able: Truth
    under_sixty: Truth
    lives_by_trade: Truth
    exercises_craft: Truth
    sufficient_resources: Truth
    occupies_own_land: Truth
    already_serving: Truth
    suitable_demand: Truth
    status: str = "free"  # Preserved metadata; O1 explicitly includes both statuses.

def recruitment_trigger(p: Recruitment) -> Truth:
    return conjunction(p.able, p.under_sixty, negation(p.lives_by_trade),
                       negation(p.exercises_craft), negation(p.sufficient_resources),
                       negation(p.occupies_own_land), negation(p.already_serving),
                       p.suitable_demand)

def early_departure_trigger(active_term: Truth, licence: Truth, cause: Truth) -> Truth:
    return conjunction(active_term, negation(disjunction(licence, cause)))

def seasonal_restriction(local_service_at_rate: Truth, august: Truth,
                         protected_custom: Truth) -> Truth:
    """S3: restriction on summer service away, for an otherwise in-scope servant.

    local_service_at_rate includes availability at the prescribed terms. False
    means this provision does not bar the move, not that all laws authorize it.
    protected_custom is an adjudicated input, not a closed county lookup.
    """
    exception = conjunction(august, protected_custom)
    return conjunction(local_service_at_rate, negation(exception))

def combined_departure_restriction(active_term: Truth, licence: Truth, cause: Truth,
                                  local_service_at_rate: Truth, august: Truth,
                                  protected_custom: Truth) -> Truth:
    """Cumulative reading, not a claim that precedence is settled by these texts."""
    return disjunction(early_departure_trigger(active_term, licence, cause),
                       seasonal_restriction(local_service_at_rate, august, protected_custom))

@dataclass(frozen=True)
class CustodyState:
    in_custody: bool
    service_obligation: Truth
    accusation: str
    acquitted: bool = False

def release_on_service_surety(s: CustodyState) -> CustodyState:
    # O3: release presupposes, rather than deletes, the commitment to serve.
    return replace(s, in_custody=False, service_obligation=True)

def acquit_presented_charge(s: CustodyState) -> CustodyState:
    # C5: do not infer a service obligation, exemption, or change in status.
    return replace(s, in_custody=False, acquitted=True)

def commission_concern(official_release: Truth, private_receipt: Truth,
                       conditions_disregarded: Truth) -> Truth:
    """D1: the conjunction singled out for inquiry; not a complete law of release."""
    return conjunction(official_release, private_receipt, conditions_disregarded)
