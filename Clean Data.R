library(plyr)
library(tidyverse)

df <- read_csv('D:/Projects/Paladins/Palastats/AllData_Long.csv')
champs <- read_csv('D:/Projects/Paladins/Palastats/AllChampions_Long.csv')
mappings <- read_csv('D:/Projects/Paladins/Palastats/mappings.csv')

# create match observation id
timestamps <- as.character(unique(df$timestamp))
ids <- 1:length(timestamps)

df_wide <- df %>% 
  mutate(id = as.character(timestamp),
         player_num = as.integer(substr(metric, nchar(metric), nchar(metric)))) %>% 
  mutate(metric = substr(metric, 0, nchar(metric)-1),
         team = ifelse(player_num %in% 0:4, 'blue', 'red'))


df_wide <- df_wide %>% 
  spread(metric, value) %>% 
  separate(details, c('map', 'gametype', 'time', 'match_id'), ' / ') %>% 
  separate(kda, c('kills', 'deaths', 'assists'), '/') %>% 
  mutate(damage = as.integer(gsub(',', '', damage)),
         healing = as.integer(gsub(',', '', healing)),
         kills = as.integer(kills),
         assists = as.integer(assists),
         deaths = as.integer(deaths),
         gametype = ifelse(gametype=='DEATHMATCH', 'DEATHMATCH', 'SIEGE'))

df_wide$id <- plyr::mapvalues(df_wide$id, from = timestamps, to = ids)

df_wide <- left_join(df_wide, mappings) # join
df_wide <- left_join(df_wide, champs) # join champion data to final dataset



write_csv(df_wide, 'D:/Projects/Paladins/Palastats/AllData_Final.csv')

#df_wide %>% 
#  select(timestamp, time) %>% 
#  mutate(fixed_time = NA) %>% 
#  filter(!duplicated(timestamp)) %>% 
#  write_csv('D:/Projects/Paladins/Palastats/mappings.csv')