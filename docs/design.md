## Flashcard Ordering
### 1. Field within Flashcard Table
**Pros**:
- Simple to implement and understand.
- Directly ties order to flashcard, making for easy retrieval.
**Cons**:
- Easy on retrieval, but each reorder requires multiple rows to be updated. This may be inefficient for large datasets. 
- Concurrency issues may arise in multi-user environments - a lock would have to acquired on the order column for every flashcard for an update.
### 2. Separate Order Column in Deck Table
**Pros**: 
- Minimizes data operations since updating a single field.
- Simplifies reorders and reduces database operations, as only one row is affected.
**Cons**:
- Serialization / deserialization overhead.
- Non-normalization can be an issue for data integrity. If a flashcard is deleted, this table would need to be updated properly, to ensure integrity.
- Handling large lists can affect performance.
### Separate Ordering Table
**Approach**: Create a dedicated tale to map the order of flashcards to their deck.
**Pros**: 
- Flexibility to manage different orders.
- Isolates order data from flashcard data, potentially improving performance for updates.
- Easier to manage different orderings for different users, if that becomes a thing, or flashcards are used differently. 
- Easier for concurrency - since there are smaller, isolated transactions. 
- Performance - high, updates can be made to small parts of the data, IF read performance is indexed properly. 
**Cons**:
- Additional joins in queries, which may impact performance without proper indexing. 
- More safisticated transaction management required. 
## Updates for Position
