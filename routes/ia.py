from fastapi import APIRouter
from pydantic import BaseModel
from services.ia_generative import MoteurIA

router = APIRouter(prefix="/ia", tags=["IA"])

ia = MoteurIA()

# 🔹 RAPPORT
class RapportRequest(BaseModel):
    type: str

@router.post("/rapport")
def rapport(req: RapportRequest):
    try:
        r = ia.generer_rapport(req.type)

        anomalies = []
        if r.anomalies:
            anomalies = [vars(a) for a in r.anomalies]

        return {
            "success": True,
            "resume": r.resume,
            "score": r.score_global,
            "kpis": r.kpis,
            "anomalies": anomalies
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


# 🔹 SUGGESTIONS
@router.get("/suggestions")
def suggestions():
    try:
        return {
            "success": True,
            "suggestions": ia.suggerer_actions()
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


# 🔹 VALIDATION IA
class ValidationRequest(BaseModel):
    type_entite: str
    etat: str
    event: str

@router.post("/valider")
def valider(req: ValidationRequest):
    try:
        result = ia.valider_transition(
            req.type_entite,
            req.etat,
            req.event
        )

        return {
            "success": True,
            "result": result
        }

    except Exception as e:
        return {"success": False, "error": str(e)}