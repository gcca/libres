package domain.model

import javax.jdo.annotations.{
  IdGeneratorStrategy,
  PersistenceCapable,
  Persistent,
  PrimaryKey }

@PersistenceCapable
class User(
  @Persistent var username: String,
  @Persistent var password: String
)
