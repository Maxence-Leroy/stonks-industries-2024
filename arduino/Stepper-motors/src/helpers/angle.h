#ifndef ANGLE_H
#define ANGLE_H

class Angle
{
  private:
    double mAngle = 0;
    void adjust();

  public:
    Angle();
    Angle(double iAngle);
    Angle(double iX, double iY);
    ~Angle();

    double toDouble() const;
    double toPositiveDouble() const;

    Angle operator+(const Angle iAngle);
    Angle& operator+=(const Angle iAngle);
    Angle operator-(const Angle iAngle);
    Angle& operator-=(const Angle iAngle);
    Angle operator+(double iAngle);
    Angle operator-(double iAngle);
    Angle operator/(double a);
    Angle& operator/=(double a);
    Angle operator=(const Angle iAngle);
    Angle operator=(double iAngle);
    bool operator<(Angle b);
    bool operator>(Angle b);
    bool operator<=(Angle b);
    bool operator>=(Angle b);
    bool operator==(const Angle b) const;
};

inline Angle Angle::operator/(double a){
  return Angle(mAngle / a);
}
inline Angle& Angle::operator/=(double a){
  mAngle /= a;
  return *this;
}
inline Angle& Angle::operator+=(Angle iAngle) {mAngle += iAngle.mAngle; adjust(); return *this;}
inline Angle& Angle::operator-=(Angle iAngle) {mAngle -= iAngle.mAngle; adjust(); return *this;}

inline bool Angle::operator<(Angle b){
  return mAngle < b.mAngle;
}
inline bool Angle::operator>(Angle b){
  return mAngle > b.mAngle;
}
inline bool Angle::operator<=(Angle b){return !this->operator>(b);}
inline bool Angle::operator>=(Angle b){return !this->operator<(b);}

inline bool Angle::operator==(const Angle b) const{
  return mAngle == b.mAngle;
}

#endif