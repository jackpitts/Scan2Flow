# Training checkpoints

Future training runs save versioned weights and resumable state here or to a
user-selected artifact path. A `best` checkpoint is an example path, not a supplied
model. Keep checkpoints outside Git with their exact configuration, preprocessing,
dataset snapshot, metrics, optimizer state, and random-generator state.
