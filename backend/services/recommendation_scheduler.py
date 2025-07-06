from sqlalchemy.orm import Session
from datetime import datetime
from backend.models import Client, User, Tree, Recommendation
from backend.crud.recommendation import was_recommendation_sent_this_month, create_recommendation
from backend.schemas.recommendation import RecommendationCreate
from .mailer import send_email
from backend.database import SessionLocal

TREE_RECOMMENDATION_MONTHS = {
    "mango": 7,
    "olive": 2,
    "lemon": 3,
    "orange": 4
}

TREE_NAME_HEBREW = {
    "mango": "מנגו",
    "olive": "זית",
    "lemon": "לימון",
    "orange": "תפוז"
}

def run_recommendation_job():
    db: Session = SessionLocal()
    now = datetime.now()
    current_month = now.month

    trees = db.query(Tree).all()

    for tree in trees:
        tree_type = tree.type.strip()
        month_for_recommendation = TREE_RECOMMENDATION_MONTHS.get(tree_type)

        if month_for_recommendation and current_month == month_for_recommendation:
            already_sent = was_recommendation_sent_this_month(
                db, tree_id=tree.id, type_="דישון עונתי"
            )
            if not already_sent:
                client = tree.client
                user = client.user

                tree_name_he = TREE_NAME_HEBREW.get(tree_type, tree_type)

                subject = f"המלצה לדישון עץ {tree_name_he}"
                message = (
                    f"שלום {client.name},\n\n"
                    f"זוהי המלצה עונתית לדשן את עץ ה-{tree_name_he} שלך.\n"
                    f"דישון עונתי תורם להתפתחות העץ וליבול עשיר יותר של פירות.\n"
                    f"אם עדיין לא תיאמת עם הגנן ({user.name}), זה זמן מצוין!\n"
                    f"ניתן ליצור קשר עם הגנן במספר: {user.phone}\n\n"
                    f"בברכה,\nמערכת ניהול הגינון"
                )

                # for hebrew readers mail from right -> left.
                message_html = message.replace('\n', '<br>')

                html_message = f"""
                <html>
                <body dir="rtl" style="font-family: Arial, sans-serif; text-align: right;">
                    <p>{message_html}</p>
                </body>
                </html>
                """
                

                send_email(to_email=client.email, subject=subject, body=html_message, html=True)

                rec = RecommendationCreate(
                    type="דישון עונתי",
                    notes=f"המלצה לפי חודש {current_month} לעץ {tree_name_he}",
                    tree_id=tree.id
                )
                create_recommendation(db, rec)

    db.close()

run_recommendation_job()