import uiScriptLocale
ACCOUNT_MANAGER_START_X = 30
ACCOUNT_MANAGER_X = 30
ACCOUNT_MANAGER_Y = 12

DIFF = 100

window = {
	"name": "LoginWindow",
	"sytle": ("movable",),
	"x": 0,
	"y": 0,
	"width": SCREEN_WIDTH,
	"height": SCREEN_HEIGHT,
	"children": 
	(
		{
			"name": "BackGround",
			"type": "expanded_image",
			"x": 0,
			"y": 0,
			"image": "d:/ymir work/ui/intro/pattern/Line_Pattern.tga",
			"x_scale": float(SCREEN_WIDTH) / 800.0,
			"y_scale": float(SCREEN_HEIGHT) / 600.0,
		},
		{
			"name": "ConnectBoard",
			"type": "thinboard",
            "x": (SCREEN_WIDTH - -5) / 2 - 1,
			"y": SCREEN_HEIGHT - (230 + DIFF),
            
			"width": 165,
			"height": 150,
			"children": 
			(
				{
					"name": "Channel1Button",
					"type": "radio_button",
					"x": 10,
					"y": 10,
					"default_image": "d:/ymir work/ui/public/large_button_01.sub",
					"over_image": "d:/ymir work/ui/public/large_button_02.sub",
					"down_image": "d:/ymir work/ui/public/large_button_03.sub",  
					"color": 4294281095,
					"text": ".....",
				},
				{
					"name": "Channel2Button",
					"type": "radio_button",
					"x": 10,
					"y": 35,
					"default_image": "d:/ymir work/ui/public/large_button_01.sub",
					"over_image": "d:/ymir work/ui/public/large_button_02.sub",
					"down_image": "d:/ymir work/ui/public/large_button_03.sub",   
					"color": 4294281095,
					"text": ".....",
				},
				{
					"name": "Channel3Button",
					"type": "radio_button",
					"x": 10,
					"y": 60,
					"default_image": "d:/ymir work/ui/public/large_button_01.sub",
					"over_image": "d:/ymir work/ui/public/large_button_02.sub",
					"down_image": "d:/ymir work/ui/public/large_button_03.sub",  
					"color": 4294281095,
					"text": ".....",
				},
				{
					"name": "Channel4Button",
					"type": "radio_button",
					"x": 10,
					"y": 85,
					"default_image": "d:/ymir work/ui/public/large_button_01.sub",
					"over_image": "d:/ymir work/ui/public/large_button_02.sub",
					"down_image": "d:/ymir work/ui/public/large_button_03.sub",
					"color": 4294281095,
					"text": ".....",
				},
			),
		},
		{
			"name": "LoginBoard",
			"type": "image",
			"x": (SCREEN_WIDTH - 415) / 2 - 1,
			"y": SCREEN_HEIGHT - (230 + DIFF),
			"image": "locale/ro/ui/login/login_main.sub",
			"children": 
			(
				{	
					"name": "ID_EditLine",
					"type": "editline",
					"x": 77,
					"y": 18,
					"width": 300,
					"height": 300,
					"input_limit": 16,
					"enable_codepage": 0,
					"r": 1.0,
					"g": 1.0,
					"b": 1.0,
					"a": 1.0,
				},
				{	
					"name": "Password_EditLine",
					"type": "editline",
					"x": 77,
					"y": 45,
					"width": 300,
					"height": 300,
					"input_limit": 16,
					"secret_flag": 1,
					"enable_codepage": 0,
					"r": 1.0,
					"g": 1.0,
					"b": 1.0,
					"a": 1.0,
				},
				{	
					"name": "Pin_EditLine",
					"type": "editline",

					"x": 77,
					"y": 72,

					"width": 300,
					"height": 450,

					"input_limit": 4,
					"secret_flag": 1,
					"enable_codepage": 0,

					"r": 1.0,
					"g": 1.0,
					"b": 1.0,
					"a": 1.0,
				},
                {	
					"name": "LoginButton",
					"type": "button",
					"x": 110,
					"y": 68+30,
					"default_image": "d:/ymir work/ui/public/large_button_01.sub",
					"over_image": "d:/ymir work/ui/public/large_button_02.sub",
					"down_image": "d:/ymir work/ui/public/large_button_03.sub",
					"text": "Giriþ",
				},
                {	
					"name": "LoginExitButton",
					"type": "button",
					"x": 10,
					"y": 68+30,
					"default_image": "d:/ymir work/ui/public/large_button_01.sub",
					"over_image": "d:/ymir work/ui/public/large_button_02.sub",
					"down_image": "d:/ymir work/ui/public/large_button_03.sub",
					"text": "Çýkýþ",
				},
			),
		},
	),
}