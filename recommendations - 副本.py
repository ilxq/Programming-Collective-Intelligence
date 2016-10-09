# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


from math import sqrt

def sim_distance(prefs,person1,person2): 
  
  si={}
  for item in prefs[person1]: 
    if item in prefs[person2]: si[item]=1

  # �������û�й�֮ͬ�����򷵻�0
  if len(si)==0: return 0

  # �������в�ֵ��ƽ����
  sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) 
                      for item in prefs[person1] if item in prefs[person2]])

  return 1/(1+sum_of_squares)

# ����p1 and p2��Ƥ��ɭ���ϵ��
def sim_pearson(prefs,p1,p2):
  # �õ�˫�������۹�����Ʒ�б�
  si={}
  for item in prefs[p1]:    #�ȵó�p1���۹���
    if item in prefs[p2]: si[item]=1   #�ٻ���p1�ҳ�p2���۹���

  # �������û�й�֮ͬ�����򷵻�1
  if len(si)==0: return 0

  # ���㹲ͬ��Ʒ
  n=len(si)
  
  # ������ƫ�����
  sum1=sum([prefs[p1][it] for it in si])
  sum2=sum([prefs[p2][it] for it in si])
  
  # ��ƽ����
  sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
  sum2Sq=sum([pow(prefs[p2][it],2) for it in si])	
  
  # ��˻�֮��
  pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
  
  #����Ƥ��ɭ����ֵ
  num=pSum-(sum1*sum2/n)
  den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
  if den==0: return 0

  r=num/den

  return r

# �ӷ�ӳƫ�õ��ֵ��з�����Ϊƥ����
# ���ؽ���ĸ��������ƶȺ�����Ϊ��ѡ����
def topMatches(prefs,person,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other),other) 
                  for other in prefs if other!=person]
  scores.sort()
  scores.reverse()
  return scores[0:n]

# ����������������ֵ�ļ�Ȩƽ����Ϊĳ���ṩ����
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
  totals={}
  simSums={}
  for other in prefs:
    # �����Լ����Ƚ�
    if other==person: continue
    sim=similarity(prefs,person,other)

    # ��������ֵΪ���С��������
    if sim<=0: continue
    for item in prefs[other]:
	    
      #ֻ���Լ���δ��������ӰƬ��������
      if item not in prefs[person] or prefs[person][item]==0:
        # ���ƶ�*����ֵ
        totals.setdefault(item,0)
        totals[item]+=prefs[other][item]*sim
        #���ƶ�֮��
        simSums.setdefault(item,0)
        simSums[item]+=sim

  # �����淶���б�
  rankings=[(total/simSums[item],item) for item,total in totals.items()]

  # ���ؾ���������б�
  rankings.sort()
  rankings.reverse()
  return rankings

def transformPrefs(prefs):
  result={}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item,{})
      
      # ����Ʒ����Ա�Ե�
      result[item][person]=prefs[person][item]
  return result


def calculateSimilarItems(prefs,n=10):
  # �����ֵ䣬�Ը�������Щ��Ʒ��Ϊ���������������Ʒ
 
  result={}
  # ����ƷΪ���Ķ�ƫ�þ���ʵʩ���ô���
  itemPrefs=transformPrefs(prefs)
  c=0
  for item in itemPrefs:
    # ��Դ����ݼ�����״̬����
    c+=1
    if c%100==0: print "%d / %d" % (c,len(itemPrefs))
    # Ѱ����Ϊ�������Ʒ
    scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
    result[item]=scores
  return result

def getRecommendedItems(prefs,itemMatch,user):
  userRatings=prefs[user]
  scores={}
  totalSim={}
  # ѭ�������ɵ�ǰ�û����ֵ���Ʒ
  for (item,rating) in userRatings.items( ):

    # ѭ�������뵱ǰ��Ʒ�������Ʒ
    for (similarity,item2) in itemMatch[item]:

      # ������û��Ѿ��Ե�ǰ��Ʒ�������ۣ��������
      if item2 in userRatings: continue

      # ����ֵ�����ƶȵļ�Ȩ֮��
      scores.setdefault(item2,0)
      scores[item2]+=similarity*rating

      # ȫ�����ƶ�֮��
      totalSim.setdefault(item2,0)
      totalSim[item2]+=similarity

  # ��ÿ���ϼ�ֵ���Լ�Ȩ�ͣ����ƽ��ֵ
  rankings=[(score/totalSim[item],item) for item,score in scores.items( )]

  # �����ֵ�����ֵ��˳�򣬷������ֽ��
  rankings.sort( )
  rankings.reverse( )
  return rankings

def loadMovieLens():
  # Get movie titles
  movies={}
  for line in open(r'E:\\inotebooks\data\movielens\u.item'):
    (id,title)=line.split('|')[0:2]
    movies[id]=title
  
  # Load data
  prefs={}
  for line in open(r'E:\\inotebooks\data\movielens\u.data'):
    (user,movieid,rating,ts)=line.split('\t')
    prefs.setdefault(user,{})
    prefs[user][movies[movieid]]=float(rating)
  return prefs
