library("car")
library("pROC")
library(sjstats)
library(lmerTest)
library(MuMIn)
require(lme4)

current_dir <- getwd()

deal_data <- read.table(file = paste(current_dir, "//Feature_Responded//res.csv", sep = ""), header = TRUE, sep = ",")

deal_data.lm <- lmer(log(dialog_speed)~as.logical(active.developer) + as.logical(roles) + lexicons + as.logical(code.snippets) + as.logical(URLs) + as.logical(weekday) + as.logical(daytime) + readbility.CLI. + as.logical(user.mentions) + (1|community_id), deal_data)
summary(deal_data.lm)
r.squaredGLMM(deal_data.lm)

resolve_data_scale<- read.table(file = paste(current_dir, "//Feature_Resolved//res.csv", sep = ""), header = TRUE, sep = ",")
resolve_data_scale.lm <- glmer(Resolved~as.logical(active.developer) + as.logical(roles) + as.logical(active.respondent) + as.logical(respondent.roles) + as.logical(code.snippets) + as.logical(URLs) + as.logical(weekday) + as.logical(daytime) + scale(readbility.CLI.) + as.logical(user.mentions) + Topic + Duration + Turn + (1|CommunityID), family = binomial(), resolve_data_scale)
summary(resolve_data_scale.lm)
new_pre <- predict(resolve_data_scale.lm, resolve_data_scale)
new_roc <- roc(resolve_data_scale$Resolved, new_pre)
auc(new_roc)


