from app import db


# model for saving prediction requests
class PredictionRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    country_code = db.Column(db.String(5), nullable=True)
    city = db.Column(db.String(100), nullable=False)

    # Unique constraint on username, country_code, and city
    __table_args__ = (db.UniqueConstraint('username', 'country_code', 'city', 
                                          name='_username_country_city_uc'),)

    def __repr__(self):
        return f'<PredictionRequest {self.username} {self.country_code} {self.city}>'