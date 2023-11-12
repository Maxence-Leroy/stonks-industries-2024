#include <math.h>

#include "angle.h"

Angle::Angle()
{
  mAngle = 0;
  adjust();
}

Angle::Angle(double iAngle)
{
  mAngle = iAngle;
  adjust();
}

Angle::Angle(double iX, double iY)
{
  double norme = sqrt(pow(iX, 2) + pow(iY, 2));
  // Code pas logique pour des raisons de précisions
  // Voir Ulysse pour plus de détails
  if(iX!=0 && fabs(iY/iX)<1)
  {
    mAngle = asin(iY/norme);
    if(iX<0)
      mAngle = M_PI - asin(iY/norme);
  }
  else
  {
    mAngle = acos(iX/norme);
    if(iY<0)
      mAngle = - acos(iX/norme) - M_PI/2;
  }
}

Angle::~Angle(){}

void Angle::adjust()
{
  while (mAngle > M_PI)
    mAngle -= 2 * M_PI;
  while (mAngle < -M_PI)
    mAngle += 2 * M_PI;
}

double Angle::toDouble() const{return mAngle;}
double Angle::toPositiveDouble() const
{
  if(mAngle<0)
  {
    return mAngle + 2 * M_PI;
  }
  else
  {
    return mAngle;
  }
}
Angle Angle::operator+(Angle iAngle) {return Angle(mAngle + iAngle.mAngle);}
Angle Angle::operator-(Angle iAngle) {return Angle(mAngle - iAngle.mAngle);}
Angle Angle::operator+(double iAngle) {return Angle(mAngle + iAngle);}
Angle Angle::operator-(double iAngle) {return Angle(mAngle - iAngle);}
void Angle::operator=(Angle iAngle) {mAngle=iAngle.mAngle; adjust();}
void Angle::operator=(double iAngle) {mAngle=iAngle; adjust();}