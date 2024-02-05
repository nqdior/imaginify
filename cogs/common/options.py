model_options = {
    "Stable Diffusion XL 1.0": "stable-diffusion-xl-1024-v1-0",
    "Stable Diffusion 1.6": "stable-diffusion-v1-6",
}

sampler_options = {
    "DDIM": 0,
    "DDPM": 1,
    "K_EULER": 2,
    "K_EULER_ANCESTRAL": 3,
    "K_HEUN": 4,
    "K_DPM_2": 5,
    "K_DPM_2_ANCESTRAL": 6,
    "K_LMS": 7,
    "K_DPMPP_2S_ANCESTRAL": 8,
    "K_DPMPP_2M": 9,
    "K_DPMPP_SDE": 10
}

clip_guidance_preset_options = {
    "NONE": 0,
    "FAST_BLUE": 1,
    "FAST_GREEN": 2,
    "SIMPLE": 3,
    "SLOW": 4,
    "SLOWER": 5,
    "SLOWEST": 6,
}

aspect_ratio_options = {
    "square 1:1": (1024, 1024),
    "wide 21:9": (1088, 448),
    "wide 16:9": (1344, 768),
    "wide 8:5": (1280, 768),
    "wide 5:4": (960, 768),
    "wide 4:3": (1024, 768),
    "wide 3:2": (1152, 768),
    "tall 9:21": (448, 1088),
    "tall 9:16": (768, 1344),
    "tall 5:8": (768, 1280),
    "tall 4:5": (768, 960),
    "tall 3:4": (768, 1024),
    "tall 2:3": (768, 1152)
}

style_preset_options = {
    'None': 'none',
    '3D Model': '3d-model',
    'Analog Film': 'analog-film',
    'Anime': 'anime',
    'Cinematic': 'cinematic',
    'Comic Book': 'comic-book',
    'Digital Art': 'digital-art',
    'Enhance': 'enhance',
    'Fantasy Art': 'fantasy-art',
    'Isometric': 'isometric',
    'Line Art': 'line-art',
    'Low Poly': 'low-poly',
    'Modeling Compound': 'modeling-compound',
    'Neon Punk': 'neon-punk',
    'Origami': 'origami',
    'Photographic': 'photographic',
    'Pixel Art': 'pixel-art',
    'Tile Texture': 'tile-texture'
}
