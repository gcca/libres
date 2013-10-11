package domain

import javax.jdo.{
  JDOHelper,
  PersistenceManagerFactory }

object PMF {
  private val pmfInstance =
    JDOHelper.getPersistenceManagerFactory("main-manager")

  def get() = this.pmfInstance
}
