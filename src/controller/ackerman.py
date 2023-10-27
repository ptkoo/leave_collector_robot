import math

def turning(angle: int, W = 65, L = 61):
	
	A = (L/2)/math.tan(math.radians(angle))
	
	Aout = A + (W/2) if angle > 0 else A - (W/2)
	Ain = A - (W/2) if angle > 0 else A + (W/2)
	
	# Inner and Outter angles for servos
	ThetaOut = math.atan((L/2)/Aout)
	ThetaIn = math.atan((L/2)/Ain)
	
	# PWM ratio
	Hout = Aout / (math.cos(ThetaOut) * 180 / math.pi)
	Hin = Ain / (math.cos(ThetaIn) * 180 / math.pi)
	OutterRatio = Hout / (Hin + Hout)
	InnerRatio = Hin / (Hout + Hin)
	
	ThetaOut = ThetaOut * 180 / math.pi
	ThetaIn = ThetaIn * 180 / math.pi
	
	if angle < 0:
		LeftTheta = ThetaIn
		RightTheta = ThetaOut
		LeftRatio = InnerRatio
		RightRatio = OutterRatio
	else:
		RightTheta = ThetaIn
		LeftTheta = ThetaOut
		RightRatio = InnerRatio
		LeftRatio = OutterRatio
	
	
	
	return LeftTheta, RightTheta, LeftRatio, RightRatio
