1.3.3
-----
Added support to persist and retrieve cookies

1.3.2
-----
Changed the logic for persistence of state back to inputs.conf to occur directly after polling/event indexing has completed rather than waiting for the polling loop frequency sleep period to exit. This potentially deals with situations where you might terminate Splunk before the REST Mod Input has persisted state changes back to inputs.conf because it was in a sleep loop during shutdown.