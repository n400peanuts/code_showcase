Analysis of the learning routines
================

``` r
library(rio);
uninstr <- import('https://raw.githubusercontent.com/n400peanuts/code_showcase/master/uninstrLearning.txt')
```

``` r
instr <- import('https://raw.githubusercontent.com/n400peanuts/code_showcase/master/instrLearning.txt', fill = T);
```

#### Performance of Uninstructed learning

``` r
temp1 <- aggregate(Acc~Subject+Blocco, data=uninstr, FUN=mean);

par(mfrow=c(1,2));
boxplot(temp1$Acc ~ temp1$Blocco, range=1, outline=F, bty='n', ylim=c(.40,1), xlab='Blocks', ylab='accuracy', notch=F, axes=F)
axis(1, at=c(1,5,10,15))
axis(2, at=seq(.40,1,.10))

myPalette <- grey(seq(0,0.8,.02))
plot(temp1$Acc[temp1$Subject==17] ~ temp1$Blocco[temp1$Subject==17], pch=19, type='b', ylim=c(.30,1), bty='n', xlab='Blocks', ylab='accuracy', axes=F)
axis(1, at=c(1,5,10,15))
axis(2, at=seq(.30,1,.10))
counter <- 2;
for (i in unique(temp1$Subject)) 
{
  lines(temp1$Acc[temp1$Subject==i] ~ temp1$Blocco[temp1$Subject==i], pch=19, type='b', col=myPalette[counter]);
  counter<-counter+1
  abline(h=.50, col='red', lwd=2);
}
```

![](learning_routine_analysis_files/figure-markdown_github/unnamed-chunk-3-1.png)

``` r
par(mfrow=c(1,1));
```

#### Performance of Instructed learning

``` r
library(ggplot2);
library(ggpubr);
```

    ## Loading required package: magrittr

``` r
dataInstr <- aggregate(Acc~Subject+Blocco, data=instr, FUN=mean); 

ggboxplot(dataInstr, x= "Blocco", y = "Acc", combine = T,
          add = "jitter", add.params = list(size = 0.1, jitter = 0.2))
```

![](learning_routine_analysis_files/figure-markdown_github/unnamed-chunk-4-1.png)
