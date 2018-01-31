import matplotlib.pyplot as plt
import time
from datetime import datetime
from mpl_toolkits.mplot3d import Axes3D
import pylab
import numpy
import os.path
import sys
import tempfile
import subprocess
import math

stockSymbol = raw_input("STOCK SYMBOL: ")
initialBank = int(raw_input("BANK ACCOUNT: "))
transactionFee = float(raw_input("TRANSACTION FEE: "))

stockDownloadScript = 'wget -O /home/brandon/Documents/DJIA/' + stockSymbol + '.csv -P /home/brandon/Documents/DJIA/ http://ichart.finance.yahoo.com/table.csv?s=' + stockSymbol + '&d=11&e=23&f=2013&g=d&a=2&b=19&c=2008&ignore=.csv'

def run_script(script):
    with tempfile.NamedTemporaryFile() as scriptfile:
        scriptfile.write(script)
        scriptfile.flush()
        subprocess.call(['/bin/bash', scriptfile.name])

if not os.path.exists('C:\\Users\\Nodnarb\\Google Drive\\Programs\\DJIA\\' + stockSymbol + '.csv'):
    print 'Downloading File...'
    run_script(stockDownloadScript)
    while(os.path.exists('/home/brandon/Documents/DJIA/' + stockSymbol + '.csv') == False):
        time.sleep(0.5)

number_plots = 1 #must be a perfect square
number_columns = int(math.ceil(number_plots**(1/2.0)))
number_rows = int(math.ceil(number_plots**(1/2.0)))
daysdec_number = 4
intervalLength = 90
finalDay = 3400 #126 - First day of trading in 2013
dateV = []
openV = []
highV = []
lowV = []
closeV = []
transactions = [] ##Date, Buy Price, cleared?, daynumber
DOHLC = []
perc = []
KE = []
histdays = []
ROI = []
lines=[0] * 4
colors = ['b', 'g', 'r', 'c', 'm', 'y']
##transactionFee = 6.95
##initialBank = 500


readFile = open('C:\\Users\\Nodnarb\\Google Drive\\Programs\\DJIA\\' + stockSymbol +'.csv', 'r')
readFile.readline()
sepFile = readFile.read().rstrip('\n').split('\n')

readFile.close()

for dayValues in sepFile:
    OHLC = dayValues.split(',')
    dateV.append(datetime.strptime(OHLC[0],"%Y-%m-%d"))
    openV.append(float(OHLC[1]))
    highV.append(float(OHLC[2]))
    lowV.append(float(OHLC[3]))
    closeV.append(float(OHLC[4]))
    DOHLC.append([OHLC[0],float(OHLC[1]),float(OHLC[2]),float(OHLC[3]),float(OHLC[4])])

def checkSeqDec(numDaysCSD, dayCheckCSD, DOHLCCSD = []):
    for dayCSD in range(numDaysCSD):    #0,1,2,3,...,numDaysCSD-1
        if DOHLCCSD[dayCheckCSD + dayCSD][1] >= DOHLCCSD[dayCheckCSD + dayCSD + 1][1]:
            return False
    return True

fig, ax = plt.subplots(number_rows, number_columns, figsize=(15,6), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = 0.15, wspace = 0.3)
ax = ax.ravel()
fig.suptitle(stockSymbol + ' Return on Investment vs. Percent Increase; 90 Day Periods', fontsize=14)

for k in range(number_plots):
	n=len(DOHLC)-2
	bankAcc = 0
	spent = 0
	perc[:]=[]
	ROI[:]=[]
	lines = [0]*4
	for dec in range(daysdec_number):
		perc[:]=[]
		ROI[:]=[]
		ROImax = -2147483649
		for percInc in range(50):
			for day in range(finalDay+k*intervalLength+intervalLength, finalDay+k*intervalLength,-1):
				if checkSeqDec(dec, day, DOHLC) and math.floor((bankAcc - transactionFee)/DOHLC[day][1]) > 0:  ##Buy Conditions
					numberOfShares = math.floor((bankAcc - transactionFee)/DOHLC[day][1])
					transactions.append([DOHLC[day][0],DOHLC[day][1],0,day,numberOfShares])
					bankAcc = bankAcc - numberOfShares * DOHLC[day][1] - transactionFee
					spent = spent + numberOfShares * DOHLC[day][1] + transactionFee
				for trans in range(len(transactions)):
					if DOHLC[day][3] > (1 + (float(percInc)/100)) * transactions[trans][1] and transactions[trans][2] == 0:  ##Sell Conditions
						transactions[trans][2] = 1
						bankAcc = bankAcc + transactions[trans][4] * DOHLC[day][3] - transactionFee
						spent = spent + transactionFee
						transactions[trans][4] = 0
			
			for trans in range(len(transactions)):
				if transactions[trans][2] == 0:
					bankAcc = bankAcc + DOHLC[0][3]
			if spent > 0:
				ROI.append(bankAcc/spent)
				if bankAcc/spent > ROImax:
					ROImaxperc = percInc
					ROImax = bankAcc/spent
			if spent == 0:
				ROI.append(0)
				if 0 > ROImax:
					ROImaxperc = percInc
					ROImax = 0
			perc.append(percInc)
			bankAcc = initialBank
			spent = 0
			transactions[:]=[]
		##print len(perc)
		##print len(ROI)
		lines[dec], = ax[k].plot(perc, ROI, color = colors[dec], label = str(dec+1) + ' Day Dec')
		ax[k].axvline(x=ROImaxperc, ymin=0, ymax=1, color=colors[dec], ls=':')
		ax[k].set_title(str(DOHLC[finalDay+k*intervalLength+intervalLength][0]) + ' to ' + str(DOHLC[finalDay+k*intervalLength][0]), fontsize=8)#'ROI Maximizing of ' + stockSymbol + ': ' + str(k*90) + ' to ' + str(k*90+90) + ' Days'
	ax[k].set_xlabel('') #'Percent Increase'
	ax[k].set_ylabel('') #'ROI'
	ax[k].plot([min(perc),max(perc)],[0,0], color = 'black')
	##ax[k].legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)
	ax[k].set_xticks([]) #numpy.arange(0,50,10)
	##ax[k].set_yticks([])

fig.legend((lines[0], lines[1], lines[2], lines[3]),('1 Day Dec','2 Day Dec','3 Day Dec','4 Day Dec'), 'lower left')
		
# # for day in range(n):
    # # KE.append(0.5*(DOHLC[day][1] ** 3 - 2 * (DOHLC[day][1] ** 2) * DOHLC[day+1][1] + DOHLC[day][1] * (DOHLC[day+1][1] ** 2)))
    # # histdays.append(datetime.strptime(DOHLC[day][0],"%Y-%m-%d"))

# # ax1 = fig.add_subplot(411)
# # ax1.plot(dateV,lowV)
# # ax1.set_title('Historical Prices of ' + stockSymbol)
# # ax1.set_xlabel('Date')
# # ax1.set_ylabel('Price')

# # ax2.set_title('ROI Maximizing of ' + stockSymbol + ': Passed 90 Days')
# # ax2.set_xlabel('Percent Increase')
# # ax2.set_ylabel('ROI')
# # ax2.plot([min(perc),max(perc)],[0,0], color = 'black')
# # ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)
# # ax2.set_xticks(numpy.arange(0,50,2))

# # ax3 = fig.add_subplot(412)
# # ax3.plot(histdays,KE)
# # ax3.set_title('Kinetic Energy Representation of ' + stockSymbol)
# # ax3.set_ylabel('Energy')
# # ax3.set_xlabel('Date')
# # ax3.plot([min(histdays),max(histdays)],[0,0], color = 'black')

# # labels = ax1.get_xticklabels()
# # for label in labels:
    # # label.set_rotation(90)

# # plt.tight_layout(pad=0.5, w_pad=0.8, h_pad=1.0)

plt.show()