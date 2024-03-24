INSERT INTO flashcards (deck_id, question, answer) VALUES ((SELECT id from decks WHERE name='Deck 1'), 'What is the role of Ingress controller in Kubernetes?', 'In Kubernetes, the Ingress controller is responsible for fulfilling the Ingress, usually with a load balancer, though it can also configure your edge router or additional frontends to help handle the traffic.');
INSERT INTO flashcards (deck_id, question, answer) VALUES ((SELECT id from decks WHERE name='Deck 1'), 'How does Ingress control external access to services in a Kubernetes cluster?', 'Ingress in Kubernetes manages external access to services in a cluster by routing external HTTP or HTTPS requests to internal services based on defined rules.');
INSERT INTO flashcards (deck_id, question, answer) VALUES ((SELECT id from decks WHERE name='Deck 1'), 'What are the differences between Ingress and Service in Kubernetes?', 'Ingress is a collection of routing rules that govern how external users access services running in a Kubernetes cluster. Service, on the other hand, is an abstraction that defines a logical set of pods and a policy to access them.');
INSERT INTO flashcards (deck_id, question, answer) VALUES ((SELECT id from decks WHERE name='Deck 1'), 'What are the benefits of using Service Discovery in Kubernetes?', 'Service Discovery in Kubernetes provides a flexible and scalable way for services to find and communicate with each other. It allows services to be loosely coupled, enhances service availability, and enables load balancing.');
INSERT INTO flashcards (deck_id, question, answer) VALUES ((SELECT id from decks WHERE name='Deck 1'), 'Why is it necessary to use Ingress in a Kubernetes cluster?', 'Ingress is necessary in a Kubernetes cluster to efficiently manage access to services from outside the cluster. It provides load balancing, SSL termination, and name-based virtual hosting.');