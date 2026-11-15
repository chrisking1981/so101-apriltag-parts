# Modellen

- base.py bouwt de cameravoet met twee sleuven.
- left_panel.py en right_panel.py bouwen de gespiegelde markerpanelen.
- assembly.py toont de gemonteerde onderdelen.
- print_layout.py toont de printoriëntaties.
- ../build_and_verify.py exporteert de drie STL's met de native OCCT exporter en controleert geometrie, meshes en assemblage-interferentie.

Python gebruikt cadgen 0.5.1, build123d 0.10.0, cadquery-ocp 7.9.3.1.1, ocp-gordon 0.1.17 en trimesh. CADGEN_DAEMON=0 voorkomt hergebruik van oude runtime-imports.
