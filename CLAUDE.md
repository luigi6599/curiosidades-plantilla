# CLAUDE.md — Plantilla "Curiosidades" (Shorts animados estilo Ricks Clips)

Esta plantilla produce YouTube Shorts de curiosidades en español, de 25-45 s, con stickmen 2D animados sobre fondos ilustrados vibrantes, cortes rápidos y subtítulos palabra por palabra. Cada Short sale de un tema, un guion, una voz, 11 escenas animadas y un montaje final.

Responde siempre en español.

## Reglas fijas del canal

- Solo Shorts verticales 9:16, 1080x1920, 30 fps.
- Sin llamada a suscribirse, sin intro y sin outro. El vídeo termina de golpe.
- Sin música de fondo por defecto: solo la voz del usuario. Añadir música solo si lo pide.
- Calidad máxima: exportar con x264 CRF 14, sin tope de bitrate, audio AAC 192k. Nunca comprimir de más.
- Cada vídeo lleva zoom o movimiento de cámara y un corte con destello corto. Nunca una presentación estática.
- Con cada Short entregar siempre: el vídeo, la portada, el título, la descripción con tiempos (capítulos) y las etiquetas listas para pegar.
- Guardar cada Short en su carpeta del ordenador del usuario, dentro de la carpeta Curiosidades (por ejemplo "Short 2"), además de enviarlo por el chat.
- Las portadas deben variar de un Short a otro (escena, composición y tipografía). El texto va arriba, nunca abajo ni sobre la cara del personaje.

## Estilo visual (ADN Ricks Clips)

- Stickman 2D: cabeza redonda color melocotón-naranja, contorno negro grueso, extremidades tubulares, ojos grandes y expresivos.
- Fondos con ilustración cel-shaded, colores muy saturados y luz de contorno fuerte.
- Planos de 2-3 s, cortes rápidos, subtítulos en negrita palabra por palabra.
- Referencias: Ricks Clips (@RicksClips3000) para el estilo visual y XpressTV (@XpressTV) para el tema y la estructura ("¿Por qué...?" de ciencia cotidiana).
- Nunca imágenes semirrealistas ni 3D: el usuario las rechazó.

## Flujo de producción

1. **Tema y guion.** Elegir una pregunta cotidiana ("¿Por qué...?"). Escribir 80-110 palabras con tono hablado y natural: gancho en la primera frase, explicación en 3 bloques, cierre con un dato que se recuerde. Sin invitación a suscribirse. Entregar el guion en el chat como texto limpio, solo narración, sin títulos ni acotaciones, con saltos de párrafo, listo para copiar en ElevenLabs.
2. **Voz.** El usuario genera el audio en ElevenLabs con su voz clonada y lo sube. Transcribir con faster-whisper (modelo "small", `word_timestamps=True`). Si falla `av.open`, decodificar antes con `ffmpeg -ac 1 -ar 16000 -f f32le` y pasar un array numpy, ejecutando con `python3 -I`. Pedir al usuario que escuche cualquier frase que Whisper entienda distinto del guion.
3. **Escenas.** Dividir la narración en unas 11 escenas según las pausas de la voz. Anotar la duración de cada una.
4. **Imágenes en Google Flow** (flow.google.com, navegador integrado). Modelo Nano Banana, 9:16, x1 (0 puntos). Primero crear un personaje de referencia y adjuntarlo en cada escena, porque la referencia se borra tras cada envío. Prompt tipo: "Using the exact same stickman character from the reference image (peach-orange round bean-shaped head, bold black outline, tubular limbs, big expressive eyes), [escena], saturated colors, strong rim light, web-animation explainer style, vertical 9:16, no text, no letters, no watermark, keep the lower third of the frame simple and uncluttered". Revisar cada imagen antes de usarla y corregir el prompt si hay errores.
5. **Vídeo en Flow.** Veo 3.1 Lite, modo Fotogramas, la imagen como fotograma de inicio, 9:16, x1: 10 puntos por clip de 8 s. Son más baratos que Omni a 720p. Prompt específico con tiempos: la acción termina en los primeros segundos y después mantiene la pose, sin cortes de cámara, sin texto, sin subtítulos, sin voz y sin música. Enviar uno cada 10-12 s. Si aparece "actividad inusual", esperar y reintentar una vez con el botón de reintento; no esquivarlo. No repetir clips sin avisar del gasto.
6. **Descarga.** Abrir cada clip en el visor de Flow y leer `document.querySelector('video').currentSrc` con JavaScript. Descargar esa URL con `curl` desde el espacio de trabajo. Comprobar los clips por fotogramas con ffmpeg antes de montar. El audio generado se descarta.
7. **Montaje con ffmpeg.**
   - Cada escena se recorta a su duración. Si la acción dura menos, ralentizar con `setpts` y `minterpolate`; si dura más, acelerar.
   - Escalar a 1080x1920 con lanczos y aplicar zoom suave (entrada o salida, alternando) con `scale ... eval=frame` más `crop`.
   - Destello blanco de 3 frames al inicio de cada escena.
   - Subtítulos ASS: fuente Inter Black 104, mayúsculas, blanco con borde negro de 10, una palabra cada vez con pequeño "pop", margen inferior 330. Usar el texto del guion, no el de Whisper.
   - Audio: solo la voz, con `loudnorm=I=-14:TP=-1.5`.
   - Codificar con CRF 14.
8. **Portada.** Fotograma de la escena 1 a 1080x1920 con el texto clave arriba (dos líneas, Inter Black, blanco y amarillo, borde negro grueso). La miniatura y el título deben complementarse, sin repetirse.
9. **Entrega.** Enviar vídeo y portada con SendUserFile y copiarlos a la carpeta Curiosidades del usuario con `device_commit_files`. Incluir título, descripción con capítulos y etiquetas.

## Control de costes

- Presupuesto por Short: unos 110 puntos de Flow (11 clips x 10).
- Probar la escena 1 primero, revisarla y solo entonces lanzar el resto, de una en una.
- Avisar antes de gastar puntos en repeticiones.
- Preguntar el saldo de puntos si no se conoce.

## Formato de la descripción

```
[Frase gancho con emoji]. [Una línea de qué se descubre].

0:00 [Capítulo 1]
0:08 [Capítulo 2]
0:18 [Capítulo 3]
0:28 [Capítulo 4]

#curiosidades #[tema] #sabiasque
```

Las etiquetas van aparte, separadas por comas, listas para pegar.

## Proyecto de ejemplo ya hecho

Short 1: "¿Por qué se nos pone la piel de gallina?" (38,7 s, 11 escenas). Duraciones por escena: 3,1 / 2,8 / 2,1 / 3,3 / 4,4 / 3,1 / 3,2 / 3,0 / 3,1 / 5,4 / 5,3 s. Úsalo como modelo de ritmo y estructura.

## Lecciones aprendidas

- Si el usuario dice "no me gusta el estilo", cambiar de estilo por completo (no retocar) y enseñar primero una prueba pequeña.
- Los vídeos deben ser clips animados, no imágenes con zoom.
- El visor de Flow tarda en abrir; esperar unos segundos y comprobar la URL antes de leer el vídeo.
- Las miniaturas del grid de Flow no se reproducen: para revisar movimiento hay que descargar el clip y mirar fotogramas.
- Los clips duran unos 7,9 s pero la acción útil suele estar en los primeros 3-4 s; después algunos clips cambian de plano, así que recortar antes.

## Scripts incluidos (carpeta scripts/)

- `transcribir.py voz.mp3 palabras.json`: transcribe la voz con Whisper y guarda cada palabra con su tiempo.
- `montar_short.py proyecto.json`: hace el montaje completo (recortes, zoom, destellos, subtítulos palabra a palabra, voz normalizada, CRF 14). Copia `ejemplo/proyecto.json`, ajusta las escenas (`src_fin` = segundos útiles del clip, `dur` = duración en el vídeo) y las correcciones de palabras que Whisper entienda mal (`{"t": segundo, "texto": "palabra del guion"}`).
- Los clips deben llamarse `escena01.mp4`, `escena02.mp4`... dentro de la carpeta `clips_dir`.
- Si alguna vez falla un paso, no repetirlo a ciegas: leer el error, arreglar y volver a lanzar solo lo que falta.

## Instalación con un solo comando

Repositorio: https://github.com/luigi6599/curiosidades-plantilla

- Windows (PowerShell): `iwr https://raw.githubusercontent.com/luigi6599/curiosidades-plantilla/main/descargar.ps1 | iex`
- Mac/Linux: `curl -fsSL https://raw.githubusercontent.com/luigi6599/curiosidades-plantilla/main/descargar.sh | bash`

Después, abre Claude en la carpeta `Curiosidades` creada y sigue este archivo.
