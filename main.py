import pymem
import time

class offsetmanager:

	#// Client
	dwLocalPlayer				= 14575972
	dwEntityList 				= 81772116
	dwClientState 				= 5894548

	#// Player
	m_hMyWeapons 				= 11784

	#// Base attributable 
	m_flFallbackWear 			= 12768
	m_nFallbackPaintKit 		= 12760
	m_nFallbackSeed 			= 12764
	m_nFallbackStatTrak 		= 12772
	m_iItemDefinitionIndex 		= 12218
	m_iItemIDHigh 				= 12240
	m_iEntityQuality 			= 12220
	m_iAccountID 				= 12248
	m_OriginalOwnerXuidLow 		= 12752

offsets = offsetmanager()

def GetWeaponPaint(itemDefinition):
	if itemDefinition == 1:
		return 711 #// Deagle
	elif itemDefinition == 4:
		return 38 #// Glock
	elif itemDefinition == 7:
		return 490 #// AK47
	elif itemDefinition == 9:
		return 344 #// AWP
	elif itemDefinition == 61:
		return 653
	else:
		return 0


def main():
	pm = pymem.Pymem('csgo.exe')

	for module in list(pm.list_modules()):
		if module.name == 'client.dll':
			global client
			client = module.lpBaseOfDll
			out.debug(client)
		if module.name == 'engine.dll':
			global engine
			engine = module.lpBaseOfDll
			out.debug(engine)

	while True:
		time.sleep(0.02)

		localPlayer: int = pm.read_uint(client + offsets.dwLocalPlayer)
		weapons: int = pm.read_uint(localPlayer + offsets.m_hMyWeapons)

		for handle in weapons:
			weapon = list()
			for wep in range(8): 
				weapon.append(pm.read_uint(client + offsets.dwEntityList + (handle and 4095) * 16 - 16))

			if paint: int = GetWeaponPaint(pm.read_short(weapon + offsets.m_iItemDefinitionIndex))
			shouldUpdate: bool = pm.read_uint32(weapon + offsets.m_nFallbackPaintKit) != paint
			
			pm.write_uint(weapon + offsets.m_iItemIDHigh, -1)
			pm.write_uint(weapon + offsets.m_nFallbackPaintKit, paint)
			pm.write_float(weapon + offsets.m_flFallbackWear, 0.1)

			pm.write_uint(weapon + offsets.m_nFallbackSeed, 0)
			pm.write_uint(weapon + offsets.m_nFallbackStatTrak, 1337)
			pm.write_uint(weapon + offsets.m_iAccountID, pm.read_uint(weapon + offsets.m_OriginalOwnerXuidLow))


			if (shouldUpdate):
				pm.write_uint(engine + offsets.dwClientState) + 372, -1


if "__name__" == "__main__":
	main()
