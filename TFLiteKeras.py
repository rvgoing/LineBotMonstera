import tensorflow as tf

# Load original model
model = tf.keras.models.load_model('best_model.keras')

# Convert to TFLite with float16 quantization
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.float16]
tflite_model = converter.convert()

# Save the smaller model
with open('best_model_fp16.tflite', 'wb') as f:
    f.write(tflite_model)
